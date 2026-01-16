from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from utils.jwt_handler import require_auth, TokenData, get_current_user
from models.todo_model import Todo, TodoCreate, TodoUpdate
from api.todo_storage import create_todo, get_todos_by_user, get_todo_by_id, update_todo, delete_todo
import uuid

router = APIRouter(prefix="/todos", tags=["todos"])

@router.post("/", response_model=Todo)
async def create_todo_endpoint(
    todo_create: TodoCreate,
    current_user: TokenData = Depends(get_current_user)
):
    """Create a new todo for the authenticated user"""
    todo = create_todo(todo_create, current_user.user_id)
    return todo

@router.get("/", response_model=List[Todo])
async def get_user_todos(
    current_user: TokenData = Depends(get_current_user)
):
    """Get all todos for the authenticated user"""
    todos = get_todos_by_user(current_user.user_id)
    return todos

@router.get("/{todo_id}", response_model=Todo)
async def get_todo(
    todo_id: str,
    current_user: TokenData = Depends(get_current_user)
):
    """Get a specific todo by ID for the authenticated user"""
    todo = get_todo_by_id(todo_id, current_user.user_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found or you don't have permission to access it"
        )
    return todo

@router.put("/{todo_id}", response_model=Todo)
async def update_todo_endpoint(
    todo_id: str,
    todo_update: TodoUpdate,
    current_user: TokenData = Depends(get_current_user)
):
    """Update a specific todo for the authenticated user"""
    # First check if the todo exists and belongs to the user
    existing_todo = get_todo_by_id(todo_id, current_user.user_id)
    if not existing_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found or you don't have permission to update it"
        )

    updated_todo = update_todo(todo_id, todo_update, current_user.user_id)
    if not updated_todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found"
        )
    return updated_todo

@router.delete("/{todo_id}")
async def delete_todo_endpoint(
    todo_id: str,
    current_user: TokenData = Depends(get_current_user)
):
    """Delete a specific todo for the authenticated user"""
    success = delete_todo(todo_id, current_user.user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found or you don't have permission to delete it"
        )
    return {"message": "Todo deleted successfully"}

# Additional user-specific endpoints for demonstration
@router.get("/count", response_model=dict)
async def get_todo_count(
    current_user: TokenData = Depends(get_current_user)
):
    """Get the count of todos for the authenticated user"""
    todos = get_todos_by_user(current_user.user_id)
    return {"count": len(todos)}

@router.delete("/", response_model=dict)
async def delete_all_user_todos(
    current_user: TokenData = Depends(get_current_user)
):
    """Delete all todos for the authenticated user"""
    user_todos = get_todos_by_user(current_user.user_id)
    count = len(user_todos)

    # Delete all todos belonging to the user
    for todo in user_todos:
        delete_todo(todo.id, current_user.user_id)

    return {"message": f"{count} todos deleted successfully"}