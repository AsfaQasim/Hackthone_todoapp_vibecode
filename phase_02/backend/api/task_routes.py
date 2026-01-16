from fastapi import APIRouter, HTTPException, status, Depends
from sqlmodel import Session, select
from typing import List
from utils.db import get_session
from models.todo_models import Task, TaskCreate, TaskUpdate, TaskRead
from utils.jwt_handler import verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter(tags=["tasks"])
security = HTTPBearer()

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get the current user ID from the JWT token"""
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id

@router.post("/api/tasks", response_model=TaskRead)
async def create_task(
    task: TaskCreate,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the logged-in user
    """
    # Create task with the current user's ID
    db_task = Task(
        title=task.title,
        completed=task.completed,
        user_id=current_user_id
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.get("/api/tasks", response_model=List[TaskRead])
async def get_tasks(
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the logged-in user
    """
    statement = select(Task).where(Task.user_id == current_user_id)
    tasks = session.exec(statement).all()
    return tasks

@router.put("/api/tasks/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: str,
    task_update: TaskUpdate,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Update a task for the logged-in user
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user_id)
    db_task = session.exec(statement).first()
    
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    # Update task fields
    if task_update.title is not None:
        db_task.title = task_update.title
    if task_update.completed is not None:
        db_task.completed = task_update.completed
    
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.delete("/api/tasks/{task_id}")
async def delete_task(
    task_id: str,
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """
    Delete a task for the logged-in user
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == current_user_id)
    db_task = session.exec(statement).first()
    
    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    session.delete(db_task)
    session.commit()
    return {"message": "Task deleted successfully"}