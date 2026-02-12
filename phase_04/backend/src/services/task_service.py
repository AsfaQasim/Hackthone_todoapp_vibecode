"""Task service for the AI Chatbot with MCP application."""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from src.models.base_models import Task, User, TaskStatus


class TaskService:
    """Service for managing tasks."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_task(self, user: User, title: str, description: Optional[str] = None) -> Task:
        """
        Create a new task for the user.
        
        Args:
            user: The user creating the task
            title: The task title
            description: Optional task description
            
        Returns:
            The created Task object
        """
        task = Task(
            title=title,
            description=description,
            user_id=user.id,
            status=TaskStatus.PENDING
        )
        
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        
        return task
    
    def get_user_tasks(self, user: User, status: Optional[str] = None) -> List[Task]:
        """
        Get all tasks for a user, optionally filtered by status.
        
        Args:
            user: The user whose tasks to retrieve
            status: Optional status filter ('pending', 'in_progress', 'completed')
            
        Returns:
            List of Task objects
        """
        query = self.db.query(Task).filter(Task.user_id == user.id)
        
        if status:
            query = query.filter(Task.status == status)
        
        return query.order_by(Task.created_at.desc()).all()
    
    def get_task_by_id(self, user: User, task_id: str) -> Optional[Task]:
        """
        Get a specific task by ID for the user.
        
        Args:
            user: The user requesting the task
            task_id: The ID of the task to retrieve
            
        Returns:
            The Task object if found and owned by the user, None otherwise
        """
        task = self.db.query(Task).filter(Task.id == task_id, Task.user_id == user.id).first()
        return task
    
    def update_task(self, user: User, task_id: str, **updates) -> Optional[Task]:
        """
        Update a task with the provided fields.
        
        Args:
            user: The user updating the task
            task_id: The ID of the task to update
            **updates: Fields to update (title, description, status, etc.)
            
        Returns:
            The updated Task object if successful, None if not found or not owned by user
        """
        task = self.get_task_by_id(user, task_id)
        if not task:
            return None
        
        # Update allowed fields
        allowed_fields = {'title', 'description', 'status'}
        for field, value in updates.items():
            if field in allowed_fields:
                setattr(task, field, value)
        
        # If status is being updated to completed, set completed_at
        if 'status' in updates and updates['status'] == TaskStatus.COMPLETED:
            task.completed_at = datetime.utcnow()
        elif 'status' in updates and updates['status'] != TaskStatus.COMPLETED:
            task.completed_at = None  # Reset completed_at if task is reopened
        
        self.db.commit()
        self.db.refresh(task)
        
        return task
    
    def delete_task(self, user: User, task_id: str) -> bool:
        """
        Delete a task.
        
        Args:
            user: The user deleting the task
            task_id: The ID of the task to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        task = self.get_task_by_id(user, task_id)
        if not task:
            return False
        
        self.db.delete(task)
        self.db.commit()
        
        return True
    
    def complete_task(self, user: User, task_id: str) -> Optional[Task]:
        """
        Mark a task as completed.
        
        Args:
            user: The user completing the task
            task_id: The ID of the task to complete
            
        Returns:
            The updated Task object if successful, None if not found or not owned by user
        """
        return self.update_task(user, task_id, status=TaskStatus.COMPLETED)
    
    def reopen_task(self, user: User, task_id: str) -> Optional[Task]:
        """
        Reopen a completed task.
        
        Args:
            user: The user reopening the task
            task_id: The ID of the task to reopen
            
        Returns:
            The updated Task object if successful, None if not found or not owned by user
        """
        return self.update_task(user, task_id, status=TaskStatus.PENDING, completed_at=None)