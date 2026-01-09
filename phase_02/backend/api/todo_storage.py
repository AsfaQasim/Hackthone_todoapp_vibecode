from typing import Dict, List, Optional
from models.todo_model import Todo, TodoCreate, TodoUpdate
import uuid
from datetime import datetime

# In-memory storage for todos
todos_db: Dict[str, Todo] = {}

def create_todo(todo_create: TodoCreate, user_id: str) -> Todo:
    """Create a new todo for a user"""
    todo = Todo(
        id=str(uuid.uuid4()),
        user_id=user_id,
        title=todo_create.title,
        description=todo_create.description,
        completed=todo_create.completed,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    todos_db[todo.id] = todo
    return todo

def get_todos_by_user(user_id: str) -> List[Todo]:
    """Get all todos for a specific user"""
    user_todos = []
    for todo in todos_db.values():
        if todo.user_id == user_id:
            user_todos.append(todo)
    return user_todos

def get_todo_by_id(todo_id: str, user_id: str) -> Optional[Todo]:
    """Get a specific todo by ID for a specific user"""
    todo = todos_db.get(todo_id)
    if todo and todo.user_id == user_id:
        return todo
    return None

def update_todo(todo_id: str, todo_update: TodoUpdate, user_id: str) -> Optional[Todo]:
    """Update a specific todo for a user"""
    todo = get_todo_by_id(todo_id, user_id)
    if not todo:
        return None
    
    update_data = todo_update.model_dump(exclude_unset=True)
    updated_todo = todo.model_copy(update=update_data)
    updated_todo.updated_at = datetime.utcnow()
    
    todos_db[todo_id] = updated_todo
    return updated_todo

def delete_todo(todo_id: str, user_id: str) -> bool:
    """Delete a specific todo for a user"""
    todo = get_todo_by_id(todo_id, user_id)
    if not todo:
        return False
    
    del todos_db[todo_id]
    return True