from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class TaskBase(SQLModel):
    title: str = Field(min_length=1)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)
    user_id: str = Field(min_length=1)  # Using string for user_id to match JWT token format

class Task(TaskBase, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class TaskCreateBase(SQLModel):
    title: str = Field(min_length=1)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)

class TaskCreate(TaskCreateBase):
    user_id: str = Field(min_length=1)  # Backend sets this from auth token

class TaskCreateRequest(TaskCreateBase):
    """Schema for task creation requests - does not include user_id"""
    pass

class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskRead(TaskBase):
    id: str
    created_at: datetime
    updated_at: datetime