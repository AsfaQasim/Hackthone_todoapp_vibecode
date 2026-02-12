from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime
from middleware.auth_middleware import JWTBearer, verify_user_is_authenticated, verify_user_owns_resource
from models.task import Task
from database.engine import get_db


router = APIRouter()


# Pydantic models
class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class Todo(TodoBase):
    id: UUID
    user_id: str
    created_at: datetime
    updated_at: datetime


# In-memory storage for demonstration (would use database in production)
todos_db = []


@router.get("/", response_model=List[Todo], dependencies=[Depends(JWTBearer())])
def get_todos(current_user=Depends(verify_user_is_authenticated)):
    """
    Get all todos for the authenticated user
    """
    user_todos = [todo for todo in todos_db if todo['user_id'] == current_user['user_id']]
    return user_todos


@router.post("/", response_model=Todo, dependencies=[Depends(JWTBearer())])
def create_todo(todo: TodoCreate, current_user=Depends(verify_user_is_authenticated)):
    """
    Create a new todo for the authenticated user
    """
    new_todo = {
        "id": uuid4(),
        "title": todo.title,
        "description": todo.description,
        "completed": todo.completed,
        "user_id": current_user["user_id"],  # Assign to authenticated user
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    todos_db.append(new_todo)
    return new_todo


@router.get("/{todo_id}", response_model=Todo, dependencies=[Depends(JWTBearer())])
def get_todo(todo_id: UUID, current_user=Depends(verify_user_is_authenticated)):
    """
    Get a specific todo by ID for the authenticated user
    """
    for todo in todos_db:
        if todo["id"] == todo_id and todo["user_id"] == current_user["user_id"]:
            return todo
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo not found or you don't have permission to access it"
    )


@router.put("/{todo_id}", response_model=Todo, dependencies=[Depends(JWTBearer())])
def update_todo(todo_id: UUID, todo_update: TodoUpdate, current_user=Depends(verify_user_is_authenticated)):
    """
    Update a specific todo by ID for the authenticated user
    """
    for i, todo in enumerate(todos_db):
        if todo["id"] == todo_id and todo["user_id"] == current_user["user_id"]:
            updated_todo = todo.copy()
            for field, value in todo_update.dict(exclude_unset=True).items():
                updated_todo[field] = value
            updated_todo["updated_at"] = datetime.utcnow()
            todos_db[i] = updated_todo
            return updated_todo
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo not found or you don't have permission to update it"
    )


@router.delete("/{todo_id}", dependencies=[Depends(JWTBearer())])
def delete_todo(todo_id: UUID, current_user=Depends(verify_user_is_authenticated)):
    """
    Delete a specific todo by ID for the authenticated user
    """
    for i, todo in enumerate(todos_db):
        if todo["id"] == todo_id and todo["user_id"] == current_user["user_id"]:
            del todos_db[i]
            return {"message": "Todo deleted successfully"}
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Todo not found or you don't have permission to delete it"
    )


@router.delete("/", dependencies=[Depends(JWTBearer())])
def delete_all_todos(current_user=Depends(verify_user_is_authenticated)):
    """
    Delete all todos for the authenticated user
    """
    global todos_db
    todos_db = [todo for todo in todos_db if todo["user_id"] != current_user["user_id"]]
    return {"message": "All your todos have been deleted"}