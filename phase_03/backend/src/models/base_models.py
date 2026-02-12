"""Database models for the AI Chatbot with MCP application using SQLModel."""

from typing import Optional, List
from datetime import datetime
import uuid
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    name: str

class User(UserBase, table=True):
    __tablename__ = "user"  # Match actual database table name
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships commented out - tables don't exist in database yet
    # tasks: List["Task"] = Relationship(back_populates="user")
    # conversations: List["Conversation"] = Relationship(back_populates="user")

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = Field(default=TaskStatus.PENDING)

class Task(TaskBase, table=True):
    __tablename__ = "task"  # Match actual database table name
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: str = Field(foreign_key="user.id")  # Changed to str to match database
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

    # Relationship commented out - not needed for basic functionality
    # user: User = Relationship(back_populates="tasks")

class ConversationBase(SQLModel):
    title: Optional[str] = None

class Conversation(ConversationBase, table=True):
    __tablename__ = "conversations"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships commented out - tables don't exist
    # user: User = Relationship(back_populates="conversations")
    # messages: List["Message"] = Relationship(back_populates="conversation")

class MessageBase(SQLModel):
    role: MessageRole
    content: str
    metadata_json: Optional[str] = None

class Message(MessageBase, table=True):
    __tablename__ = "messages"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    conversation_id: uuid.UUID = Field(foreign_key="conversations.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    # Relationship commented out - table doesn't exist
    # conversation: Conversation = Relationship(back_populates="messages")