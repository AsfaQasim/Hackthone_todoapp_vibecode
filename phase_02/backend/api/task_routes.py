from fastapi import APIRouter, HTTPException, status, Depends, Path
from sqlmodel import Session
from typing import List
from utils.db import get_session
from utils.jwt_handler import require_auth, TokenData
from models.task_model import Task, TaskCreate, TaskUpdate, TaskRead
from api.task_service import (
    create_task, get_tasks_by_user, get_task_by_id_and_user, 
    update_task, delete_task, toggle_task_completion
)

router = APIRouter(prefix="/api/{user_id}", tags=["tasks"])

@router.get("/tasks", response_model=List[TaskRead])
async def list_tasks(
    user_id: str,
    current_user: TokenData = Depends(require_auth),
    session: Session = Depends(get_session)
):
    """
    List all tasks for the authenticated user.
    Ownership enforcement: Only the authenticated user can access their own tasks.
    """
    # Verify that the requested user_id matches the authenticated user_id
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot access another user's tasks"
        )
    
    tasks = get_tasks_by_user(session, user_id)
    return tasks

@router.post("/tasks", response_model=TaskRead)
async def create_new_task(
    user_id: str,
    task_create: TaskCreate,
    current_user: TokenData = Depends(require_auth),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    Ownership enforcement: Only the authenticated user can create tasks for themselves.
    """
    # Verify that the requested user_id matches the authenticated user_id
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot create tasks for another user"
        )
    
    # Ensure the task is assigned to the authenticated user
    task_create.user_id = user_id
    
    try:
        task = create_task(session, task_create)
        return task
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Error creating task: {str(e)}"
        )

@router.get("/tasks/{task_id}", response_model=TaskRead)
async def get_task(
    user_id: str,
    task_id: str = Path(..., description="The ID of the task to retrieve"),
    current_user: TokenData = Depends(require_auth),
    session: Session = Depends(get_session)
):
    """
    Get details of a specific task.
    Ownership enforcement: Only the task owner can access the task.
    """
    # Verify that the requested user_id matches the authenticated user_id
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot access another user's tasks"
        )
    
    task = get_task_by_id_and_user(session, task_id, user_id)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to access it"
        )
    
    return task

@router.put("/tasks/{task_id}", response_model=TaskRead)
async def update_existing_task(
    user_id: str,
    task_id: str = Path(..., description="The ID of the task to update"),
    task_update: TaskUpdate,
    current_user: TokenData = Depends(require_auth),
    session: Session = Depends(get_session)
):
    """
    Update a specific task.
    Ownership enforcement: Only the task owner can update the task.
    """
    # Verify that the requested user_id matches the authenticated user_id
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot update another user's tasks"
        )
    
    updated_task = update_task(session, task_id, user_id, task_update)
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to update it"
        )
    
    return updated_task

@router.delete("/tasks/{task_id}")
async def delete_existing_task(
    user_id: str,
    task_id: str = Path(..., description="The ID of the task to delete"),
    current_user: TokenData = Depends(require_auth),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task.
    Ownership enforcement: Only the task owner can delete the task.
    """
    # Verify that the requested user_id matches the authenticated user_id
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot delete another user's tasks"
        )
    
    success = delete_task(session, task_id, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to delete it"
        )
    
    return {"message": "Task deleted successfully"}

@router.patch("/tasks/{task_id}/complete", response_model=TaskRead)
async def toggle_task_completion_status(
    user_id: str,
    task_id: str = Path(..., description="The ID of the task to toggle completion for"),
    current_user: TokenData = Depends(require_auth),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a task.
    Ownership enforcement: Only the task owner can toggle completion status.
    """
    # Verify that the requested user_id matches the authenticated user_id
    if current_user.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: Cannot modify another user's tasks"
        )
    
    toggled_task = toggle_task_completion(session, task_id, user_id)
    if not toggled_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or you don't have permission to modify it"
        )
    
    return toggled_task