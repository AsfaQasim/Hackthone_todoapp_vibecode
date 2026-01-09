from sqlmodel import Session, select
from models.task_model import Task, TaskCreate, TaskUpdate
from typing import List, Optional
import uuid
from datetime import datetime

def create_task(session: Session, task_create: TaskCreate) -> Task:
    """Create a new task in the database"""
    db_task = Task(
        title=task_create.title,
        description=task_create.description,
        completed=task_create.completed,
        user_id=task_create.user_id
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def get_tasks_by_user(session: Session, user_id: str) -> List[Task]:
    """Get all tasks for a specific user"""
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return tasks

def get_task_by_id_and_user(session: Session, task_id: str, user_id: str) -> Optional[Task]:
    """Get a specific task by ID for a specific user"""
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    return task

def update_task(session: Session, task_id: str, user_id: str, task_update: TaskUpdate) -> Optional[Task]:
    """Update a specific task for a specific user"""
    # First verify the task exists and belongs to the user
    db_task = get_task_by_id_and_user(session, task_id, user_id)
    if not db_task:
        return None

    # Apply updates
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)

    db_task.updated_at = datetime.utcnow()
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

def delete_task(session: Session, task_id: str, user_id: str) -> bool:
    """Delete a specific task for a specific user"""
    db_task = get_task_by_id_and_user(session, task_id, user_id)
    if not db_task:
        return False

    session.delete(db_task)
    session.commit()
    return True

def toggle_task_completion(session: Session, task_id: str, user_id: str) -> Optional[Task]:
    """Toggle the completion status of a task"""
    db_task = get_task_by_id_and_user(session, task_id, user_id)
    if not db_task:
        return None

    db_task.completed = not db_task.completed
    db_task.updated_at = datetime.utcnow()
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task