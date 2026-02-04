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
    current_user_id = get_current_user_id(request)
    if str(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own tasks"
        )

    query = select(Task).where(Task.user_id == user_id)
    
    if status:
        if status in [s.value for s in TaskStatus]:
            query = query.where(Task.status == status)
    
    tasks = session.exec(query).all()
    return tasks


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
    current_user_id = get_current_user_id(request)
    if str(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only create tasks for yourself"
        )

    db_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        user_id=user_id # SQLModel will handle UUID conversion if string provided
    )

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


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
    current_user_id = get_current_user_id(request)
    if str(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own tasks"
        )

    query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(query).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return db_task


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
    current_user_id = get_current_user_id(request)
    if str(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only update your own tasks"
        )

    query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(query).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    task_data = task_update.model_dump(exclude_unset=True)
    for key, value in task_data.items():
        setattr(db_task, key, value)

    db_task.updated_at = datetime.utcnow()

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


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
    current_user_id = get_current_user_id(request)
    if str(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only delete your own tasks"
        )

    query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(query).first()

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
    request: Request,
    session: Session = Depends(get_db)
):
    """
    Toggle the completion status of a specific task for the authenticated user
    """
    current_user_id = get_current_user_id(request)
    if str(current_user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only modify your own tasks"
        )

    query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(query).first()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    if db_task.status == TaskStatus.COMPLETED:
        db_task.status = TaskStatus.PENDING
        db_task.completed_at = None
    else:
        db_task.status = TaskStatus.COMPLETED
        db_task.completed_at = datetime.utcnow()

    db_task.updated_at = datetime.utcnow()

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task