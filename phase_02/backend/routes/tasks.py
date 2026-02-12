from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from uuid import UUID
from datetime import datetime
from sqlmodel import Session, select
from database.engine import engine
from models.task import Task, TaskCreate, TaskUpdate, TaskResponse
from middleware.auth_middleware import JWTBearer, verify_user_is_authenticated
from database.engine import get_db

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
        statement = select(Task).where(Task.user_id == user_id)
        tasks = session.exec(statement).all()
        return tasks


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
    db_task = Task(**task.model_dump())
    db_task.user_id = user_id
    
    with Session(engine) as session:
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task


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
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        db_task = session.exec(statement).first()
        
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
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        db_task = session.exec(statement).first()
        
        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Update the task with the provided values
        task_data = task_update.model_dump(exclude_unset=True)
        for field, value in task_data.items():
            setattr(db_task, field, value)

        db_task.updated_at = datetime.utcnow()
        
        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task


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
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        db_task = session.exec(statement).first()
        
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
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        db_task = session.exec(statement).first()
        
        if not db_task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )
        
        # Toggle the completion status
        db_task.completed = not db_task.completed
        db_task.updated_at = datetime.utcnow()

        session.add(db_task)
        session.commit()
        session.refresh(db_task)
        return db_task