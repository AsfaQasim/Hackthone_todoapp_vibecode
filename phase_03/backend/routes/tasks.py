from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from sqlmodel import Session, select, func
from src.db import get_db
from src.models.base_models import Task, User, TaskStatus
from src.api.middleware.auth_middleware import auth_middleware
# Assuming verify_user_is_authenticated is available or we use auth_middleware dependency
from src.services.auth_service import verify_token # We might need to check where this is

# Pydantic models for API responses
from pydantic import BaseModel
import logging
import traceback

logger = logging.getLogger(__name__)

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None

class TaskResponse(BaseModel):
    id: UUID
    user_id: UUID
    title: str
    description: Optional[str] = None
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

router = APIRouter(prefix="/api", tags=["tasks"])

# Helper dependency to get current user from request state (set by auth_middleware)
# Or we can reuse the existing pattern if it's robust.
# The previous code used `Depends(verify_user_is_authenticated)`.
# Let's assume we can get the user from the request if the middleware runs.

from fastapi import Request

def get_current_user_id(request: Request) -> str:
    if not hasattr(request.state, "user"):
        raise HTTPException(status_code=401, detail="Not authenticated")
    return request.state.user["user_id"]

@router.get("/{user_id}/tasks", response_model=List[TaskResponse])
def list_tasks(
    user_id: str,
    request: Request,
    status: Optional[str] = None,
    session: Session = Depends(get_db)
):
    """
    List all tasks for the authenticated user
    """
    try:
        current_user_id = get_current_user_id(request)
        if str(current_user_id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You can only access your own tasks"
            )

        # Use raw SQL query to bypass SQLModel UUID conversion
        logger.info(f"Querying tasks for user_id: {user_id}")
        
        from sqlalchemy import text
        
        # First, try to get user by email to find all their tasks
        # This handles the case where login creates different user IDs
        try:
            # Get user email from token
            user_email = request.state.user.get("email") if hasattr(request.state, "user") else None
            
            if user_email:
                logger.info(f"Also checking tasks by email: {user_email}")
                
                # Get user ID from email
                user_query = text("SELECT id FROM users WHERE email = :email")
                user_result = session.execute(user_query, {"email": user_email})
                user_row = user_result.fetchone()
                
                if user_row:
                    actual_user_id = str(user_row[0])
                    logger.info(f"Found user ID from email: {actual_user_id}")
                    
                    # Use the actual user ID from database
                    query_text = text("SELECT * FROM tasks WHERE user_id = :user_id")
                    result = session.execute(query_text, {"user_id": actual_user_id})
                else:
                    # Fallback to provided user_id
                    query_text = text("SELECT * FROM tasks WHERE user_id = :user_id")
                    result = session.execute(query_text, {"user_id": user_id})
            else:
                # No email, use provided user_id
                query_text = text("SELECT * FROM tasks WHERE user_id = :user_id")
                result = session.execute(query_text, {"user_id": user_id})
        except Exception as email_error:
            logger.error(f"Error getting user by email: {email_error}")
            # Fallback to provided user_id
            query_text = text("SELECT * FROM tasks WHERE user_id = :user_id")
            result = session.execute(query_text, {"user_id": user_id})
        
        # Convert to Task objects - use index-based access for raw SQL results
        tasks = []
        for row in result:
            # Row columns: id, title, description, status, user_id, created_at, updated_at, completed_at
            task = Task(
                id=row[0],  # id
                title=row[1],  # title
                description=row[2],  # description
                status=row[3],  # status
                user_id=row[4],  # user_id
                created_at=row[5],  # created_at
                updated_at=row[6],  # updated_at
                completed_at=row[7]  # completed_at
            )
            tasks.append(task)
        
        logger.info(f"Found {len(tasks)} tasks")
        return tasks
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"List tasks error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve tasks due to an internal server error"
        )


@router.post("/{user_id}/tasks", response_model=TaskResponse)
def create_task(
    user_id: str,
    task: TaskCreate,
    request: Request,
    session: Session = Depends(get_db)
):
    """
    Create a new task for the authenticated user
    """
    try:
        current_user_id = get_current_user_id(request)
        if str(current_user_id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You can only create tasks for yourself"
            )

        # Use raw SQL to ensure user_id is stored as string
        from sqlalchemy import text
        import uuid
        task_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        query_text = text("""
            INSERT INTO tasks (id, title, description, status, user_id, created_at, updated_at)
            VALUES (:id, :title, :description, :status, :user_id, :created_at, :updated_at)
        """)
        
        session.execute(query_text, {
            "id": task_id,
            "title": task.title,
            "description": task.description,
            "status": task.status.value,
            "user_id": user_id,
            "created_at": now,
            "updated_at": now
        })
        session.commit()
        
        # Fetch the created task
        fetch_query = text("SELECT * FROM tasks WHERE id = :id")
        result = session.execute(fetch_query, {"id": task_id})
        row = result.fetchone()
        
        db_task = Task(
            id=row[0],
            title=row[1],
            description=row[2],
            status=row[3],
            user_id=row[4],
            created_at=row[5],
            updated_at=row[6],
            completed_at=row[7]
        )

        return db_task
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Create task error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create task due to an internal server error"
        )


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    user_id: str,
    task_id: UUID,
    request: Request,
    session: Session = Depends(get_db)
):
    """
    Get a specific task by ID for the authenticated user
    """
    try:
        current_user_id = get_current_user_id(request)
        if str(current_user_id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You can only access your own tasks"
            )

        from sqlalchemy import text
        query_text = text("SELECT * FROM tasks WHERE id = :task_id AND user_id = :user_id")
        result = session.execute(query_text, {"task_id": str(task_id), "user_id": user_id})
        row = result.fetchone()

        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        db_task = Task(
            id=row[0],
            title=row[1],
            description=row[2],
            status=row[3],
            user_id=row[4],
            created_at=row[5],
            updated_at=row[6],
            completed_at=row[7]
        )

        return db_task
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Get task error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve task due to an internal server error"
        )


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    user_id: str,
    task_id: UUID,
    task_update: TaskUpdate,
    request: Request,
    session: Session = Depends(get_db)
):
    """
    Update a specific task by ID for the authenticated user
    """
    try:
        current_user_id = get_current_user_id(request)
        if str(current_user_id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You can only update your own tasks"
            )

        from sqlalchemy import text
        
        # First check if task exists
        check_query = text("SELECT * FROM tasks WHERE id = :task_id AND user_id = :user_id")
        result = session.execute(check_query, {"task_id": str(task_id), "user_id": user_id})
        row = result.fetchone()

        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Build update query dynamically
        task_data = task_update.model_dump(exclude_unset=True)
        if not task_data:
            # No updates provided, return existing task
            return Task(
                id=row[0], title=row[1], description=row[2], status=row[3],
                user_id=row[4], created_at=row[5], updated_at=row[6], completed_at=row[7]
            )
        
        # Build SET clause
        set_parts = []
        params = {"task_id": str(task_id), "user_id": user_id, "updated_at": datetime.utcnow().isoformat()}
        
        for key, value in task_data.items():
            set_parts.append(f"{key} = :{key}")
            params[key] = value.value if hasattr(value, 'value') else value
        
        set_parts.append("updated_at = :updated_at")
        
        update_query = text(f"UPDATE tasks SET {', '.join(set_parts)} WHERE id = :task_id AND user_id = :user_id")
        session.execute(update_query, params)
        session.commit()

        # Fetch updated task
        result = session.execute(check_query, {"task_id": str(task_id), "user_id": user_id})
        row = result.fetchone()
        
        db_task = Task(
            id=row[0], title=row[1], description=row[2], status=row[3],
            user_id=row[4], created_at=row[5], updated_at=row[6], completed_at=row[7]
        )

        return db_task
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Update task error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task due to an internal server error"
        )


@router.delete("/{user_id}/tasks/{task_id}")
def delete_task(
    user_id: str,
    task_id: UUID,
    request: Request,
    session: Session = Depends(get_db)
):
    """
    Delete a specific task by ID for the authenticated user
    """
    try:
        current_user_id = get_current_user_id(request)
        if str(current_user_id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You can only delete your own tasks"
            )

        from sqlalchemy import text
        
        # Check if task exists
        check_query = text("SELECT * FROM tasks WHERE id = :task_id AND user_id = :user_id")
        result = session.execute(check_query, {"task_id": str(task_id), "user_id": user_id})
        row = result.fetchone()

        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Delete the task
        delete_query = text("DELETE FROM tasks WHERE id = :task_id AND user_id = :user_id")
        session.execute(delete_query, {"task_id": str(task_id), "user_id": user_id})
        session.commit()
        
        return {"message": "Task deleted successfully"}
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Delete task error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete task due to an internal server error"
        )


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
def toggle_task_completion(
    user_id: str,
    task_id: UUID,
    request: Request,
    session: Session = Depends(get_db)
):
    """
    Toggle the completion status of a specific task for the authenticated user
    """
    try:
        current_user_id = get_current_user_id(request)
        if str(current_user_id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: You can only modify your own tasks"
            )

        from sqlalchemy import text
        
        # Check if task exists
        check_query = text("SELECT * FROM tasks WHERE id = :task_id AND user_id = :user_id")
        result = session.execute(check_query, {"task_id": str(task_id), "user_id": user_id})
        row = result.fetchone()

        if not row:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Toggle completion status
        current_status = row[3]  # status column
        new_status = TaskStatus.PENDING if current_status == TaskStatus.COMPLETED else TaskStatus.COMPLETED
        completed_at = datetime.utcnow().isoformat() if new_status == TaskStatus.COMPLETED else None
        
        update_query = text("""
            UPDATE tasks 
            SET status = :status, completed_at = :completed_at, updated_at = :updated_at
            WHERE id = :task_id AND user_id = :user_id
        """)
        
        session.execute(update_query, {
            "status": new_status.value,
            "completed_at": completed_at,
            "updated_at": datetime.utcnow().isoformat(),
            "task_id": str(task_id),
            "user_id": user_id
        })
        session.commit()

        # Fetch updated task
        result = session.execute(check_query, {"task_id": str(task_id), "user_id": user_id})
        row = result.fetchone()
        
        db_task = Task(
            id=row[0], title=row[1], description=row[2], status=row[3],
            user_id=row[4], created_at=row[5], updated_at=row[6], completed_at=row[7]
        )

        return db_task
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Toggle task completion error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update task status due to an internal server error"
        )