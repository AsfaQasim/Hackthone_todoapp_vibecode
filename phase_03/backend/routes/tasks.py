from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.db import engine, get_db
from src.models.base_models import Task as DBTask, User
from src.api.middleware.auth_middleware import auth_middleware
from middleware.auth_middleware import JWTBearer, verify_user_is_authenticated

# Pydantic models for API responses
from pydantic import BaseModel
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "pending"

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None

class TaskResponse(TaskBase):
    id: UUID
    user_id: str
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

router = APIRouter(prefix="/api", tags=["tasks"])


@router.get("/{user_id}/tasks", response_model=List[TaskResponse])
def list_tasks(
    user_id: str,
    current_user=Depends(verify_user_is_authenticated)
):
    """
    List all tasks for the authenticated user
    """
    # Verify that the user_id in the path matches the authenticated user
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own tasks"
        )

    # Query the database for tasks belonging to the user
    with Session(engine) as session:
        statement = select(DBTask).where(DBTask.user_id == user_id)
        tasks = session.execute(statement).scalars().all()
        return [
            TaskResponse(
                id=task.id,
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                status=task.status,
                created_at=task.created_at,
                updated_at=task.updated_at,
                completed_at=task.completed_at
            )
            for task in tasks
        ]


@router.post("/{user_id}/tasks", response_model=TaskResponse)
def create_task(
    user_id: str,
    task: TaskCreate,
    current_user=Depends(verify_user_is_authenticated)
):
    """
    Create a new task for the authenticated user
    """
    # Verify that the user_id in the path matches the authenticated user
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only create tasks for yourself"
        )

    # Create a new task with the authenticated user's ID
    db_task = DBTask(
        title=task.title,
        description=task.description,
        status=task.status,
        user_id=user_id
    )

    with Session(engine) as session:
        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return TaskResponse(
            id=db_task.id,
            user_id=db_task.user_id,
            title=db_task.title,
            description=db_task.description,
            status=db_task.status,
            created_at=db_task.created_at,
            updated_at=db_task.updated_at,
            completed_at=db_task.completed_at
        )


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    user_id: str,
    task_id: UUID,
    current_user=Depends(verify_user_is_authenticated)
):
    """
    Get a specific task by ID for the authenticated user
    """
    # Verify that the user_id in the path matches the authenticated user
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own tasks"
        )

    with Session(engine) as session:
        statement = select(DBTask).where(DBTask.id == task_id, DBTask.user_id == user_id)
        db_task = session.execute(statement).scalars().first()

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        return TaskResponse(
            id=db_task.id,
            user_id=db_task.user_id,
            title=db_task.title,
            description=db_task.description,
            status=db_task.status,
            created_at=db_task.created_at,
            updated_at=db_task.updated_at,
            completed_at=db_task.completed_at
        )


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    user_id: str,
    task_id: UUID,
    task_update: TaskUpdate,
    current_user=Depends(verify_user_is_authenticated)
):
    """
    Update a specific task by ID for the authenticated user
    """
    # Verify that the user_id in the path matches the authenticated user
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only update your own tasks"
        )

    with Session(engine) as session:
        statement = select(DBTask).where(DBTask.id == task_id, DBTask.user_id == user_id)
        db_task = session.execute(statement).scalars().first()

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Update the task with the provided values
        task_data = task_update.model_dump(exclude_unset=True)
        for field, value in task_data.items():
            if value is not None:
                setattr(db_task, field, value)

        db_task.updated_at = datetime.utcnow()

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return TaskResponse(
            id=db_task.id,
            user_id=db_task.user_id,
            title=db_task.title,
            description=db_task.description,
            status=db_task.status,
            created_at=db_task.created_at,
            updated_at=db_task.updated_at,
            completed_at=db_task.completed_at
        )


@router.delete("/{user_id}/tasks/{task_id}")
def delete_task(
    user_id: str,
    task_id: UUID,
    current_user=Depends(verify_user_is_authenticated)
):
    """
    Delete a specific task by ID for the authenticated user
    """
    # Verify that the user_id in the path matches the authenticated user
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only delete your own tasks"
        )

    with Session(engine) as session:
        statement = select(DBTask).where(DBTask.id == task_id, DBTask.user_id == user_id)
        db_task = session.execute(statement).scalars().first()

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        session.delete(db_task)
        session.commit()
        return {"message": "Task deleted successfully"}


@router.patch("/{user_id}/tasks/{task_id}/complete", response_model=TaskResponse)
def toggle_task_completion(
    user_id: str,
    task_id: UUID,
    current_user=Depends(verify_user_is_authenticated)
):
    """
    Toggle the completion status of a specific task for the authenticated user
    """
    # Verify that the user_id in the path matches the authenticated user
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only modify your own tasks"
        )

    with Session(engine) as session:
        statement = select(DBTask).where(DBTask.id == task_id, DBTask.user_id == user_id)
        db_task = session.execute(statement).scalars().first()

        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Toggle the completion status by updating the status field
        if db_task.status == 'completed':
            db_task.status = 'pending'
            db_task.completed_at = None
        else:
            db_task.status = 'completed'
            db_task.completed_at = datetime.utcnow()

        db_task.updated_at = datetime.utcnow()

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        return TaskResponse(
            id=db_task.id,
            user_id=db_task.user_id,
            title=db_task.title,
            description=db_task.description,
            status=db_task.status,
            created_at=db_task.created_at,
            updated_at=db_task.updated_at,
            completed_at=db_task.completed_at
        )