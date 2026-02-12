"""Simplified tasks endpoint that works with JWT authentication."""

from fastapi import APIRouter, Depends, HTTPException, Header
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import logging

from src.db import get_db
from src.models.base_models import User, Task, TaskStatus

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["tasks"])


class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None


async def get_user_from_token(authorization: str = Header(None), db: Session = Depends(get_db)) -> User:
    """Get user from JWT token - simplified and working version."""
    if not authorization or not authorization.startswith("Bearer "):
        logger.error("No authorization header or invalid format")
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    token = authorization.split(" ")[1]
    
    try:
        import jwt
        from src.config import settings
        
        # Decode token
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
            logger.info(f"✅ Token decoded successfully")
        except jwt.ExpiredSignatureError:
            logger.error("❌ Token has expired")
            raise HTTPException(status_code=401, detail="Token expired")
        except Exception as e:
            logger.error(f"❌ Token decode failed: {e}")
            raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")
        
        # Get user ID from payload
        user_id = payload.get("sub") or payload.get("userId") or payload.get("user_id")
        email = payload.get("email", "unknown@example.com")
        
        if not user_id:
            logger.error("❌ No user ID in token")
            raise HTTPException(status_code=401, detail="Invalid token: no user ID")
        
        logger.info(f"🔍 Looking for user: {user_id}")
        
        # Try to find user in database
        try:
            user = db.query(User).filter(User.id == user_id).first()
            
            if user:
                logger.info(f"✅ User found: {user.email}")
                return user
            
            # Try to find by email if not found by ID
            user = db.query(User).filter(User.email == email).first()
            if user:
                logger.info(f"✅ User found by email: {user.email}")
                return user
            
            # User doesn't exist, create it
            logger.info(f"➕ User not found, creating new user: {user_id}")
            new_user = User(
                id=user_id,
                email=email,
                name=payload.get("name", email.split("@")[0])
            )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            logger.info(f"✅ New user created: {new_user.email}")
            return new_user
            
        except Exception as db_error:
            logger.error(f"❌ Database error: {db_error}")
            # Try to rollback and find user again
            db.rollback()
            user = db.query(User).filter(User.email == email).first()
            if user:
                logger.info(f"✅ User found after rollback: {user.email}")
                return user
            raise HTTPException(status_code=500, detail=f"Database error: {str(db_error)}")
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error in get_user_from_token: {e}")
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")


@router.get("/tasks")
async def list_tasks(
    current_user: User = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    """
    List all tasks for the authenticated user.
    """
    try:
        logger.info(f"=" * 60)
        logger.info(f"📋 Fetching tasks for user: {current_user.email} (ID: {current_user.id})")
        
        # Query tasks for this user
        query = select(Task).where(Task.user_id == str(current_user.id))
        tasks = db.exec(query).all()
        
        logger.info(f"✅ Found {len(tasks)} tasks")
        
        # Convert to dict for JSON response
        tasks_list = []
        for task in tasks:
            tasks_list.append({
                "id": str(task.id),
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "user_id": str(task.user_id),
                "created_at": task.created_at.isoformat() if task.created_at else None,
                "updated_at": task.updated_at.isoformat() if task.updated_at else None,
                "completed_at": task.completed_at.isoformat() if task.completed_at else None
            })
        
        logger.info(f"=" * 60)
        return tasks_list
        
    except Exception as e:
        logger.error(f"❌ Error fetching tasks: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/tasks")
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Create a new task for the authenticated user.
    """
    try:
        logger.info(f"=" * 60)
        logger.info(f"➕ Creating task for user: {current_user.email}")
        logger.info(f"   Title: {task_data.title}")
        
        # Create the task
        new_task = Task(
            title=task_data.title,
            description=task_data.description or "",
            status=TaskStatus.PENDING,
            user_id=str(current_user.id)
        )
        
        db.add(new_task)
        db.commit()
        db.refresh(new_task)
        
        logger.info(f"✅ Task created successfully!")
        logger.info(f"   ID: {new_task.id}")
        logger.info(f"=" * 60)
        
        return {
            "id": str(new_task.id),
            "title": new_task.title,
            "description": new_task.description,
            "status": new_task.status,
            "user_id": str(new_task.user_id),
            "created_at": new_task.created_at.isoformat() if new_task.created_at else None,
            "updated_at": new_task.updated_at.isoformat() if new_task.updated_at else None,
            "completed_at": None
        }
        
    except Exception as e:
        logger.error(f"❌ Error creating task: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/tasks/{task_id}")
async def update_task(
    task_id: str,
    task_data: TaskUpdate,
    current_user: User = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Update a task for the authenticated user.
    """
    try:
        logger.info(f"=" * 60)
        logger.info(f"✏️ Updating task {task_id} for user: {current_user.email}")
        
        # Find the task
        query = select(Task).where(Task.id == task_id, Task.user_id == str(current_user.id))
        task = db.exec(query).first()
        
        if not task:
            logger.error(f"❌ Task not found: {task_id}")
            raise HTTPException(status_code=404, detail="Task not found")
        
        # Update fields
        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.status is not None:
            task.status = task_data.status
            if task_data.status == "completed":
                task.completed_at = datetime.utcnow()
            else:
                task.completed_at = None
        
        task.updated_at = datetime.utcnow()
        
        db.add(task)
        db.commit()
        db.refresh(task)
        
        logger.info(f"✅ Task updated successfully!")
        logger.info(f"=" * 60)
        
        return {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "user_id": str(task.user_id),
            "created_at": task.created_at.isoformat() if task.created_at else None,
            "updated_at": task.updated_at.isoformat() if task.updated_at else None,
            "completed_at": task.completed_at.isoformat() if task.completed_at else None
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error updating task: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/tasks/{task_id}")
async def delete_task(
    task_id: str,
    current_user: User = Depends(get_user_from_token),
    db: Session = Depends(get_db)
):
    """
    Delete a task for the authenticated user.
    """
    try:
        logger.info(f"=" * 60)
        logger.info(f"🗑️ Deleting task {task_id} for user: {current_user.email}")
        
        # Find the task
        query = select(Task).where(Task.id == task_id, Task.user_id == str(current_user.id))
        task = db.exec(query).first()
        
        if not task:
            logger.error(f"❌ Task not found: {task_id}")
            raise HTTPException(status_code=404, detail="Task not found")
        
        db.delete(task)
        db.commit()
        
        logger.info(f"✅ Task deleted successfully!")
        logger.info(f"=" * 60)
        
        return {"message": "Task deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error deleting task: {e}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
