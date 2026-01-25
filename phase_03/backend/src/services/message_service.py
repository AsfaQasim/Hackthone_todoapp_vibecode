"""Message persistence layer for storing user/assistant messages in DB."""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..models.base_models import Message, Conversation
from ..services.mcp_tool_service import MCPToolResult


def store_user_message(
    db: Session, 
    conversation_id: str, 
    content: str, 
    metadata: Optional[dict] = None
) -> Message:
    """
    Store a user message in the database.
    
    Args:
        db: Database session
        conversation_id: ID of the conversation
        content: Message content
        metadata: Optional metadata for the message
        
    Returns:
        The created Message object
    """
    message = Message(
        conversation_id=conversation_id,
        role='user',
        content=content,
        metadata_json=str(metadata) if metadata else None
    )
    
    db.add(message)
    db.commit()
    db.refresh(message)
    
    return message


def store_assistant_message(
    db: Session, 
    conversation_id: str, 
    content: str, 
    tool_calls: Optional[List[dict]] = None
) -> Message:
    """
    Store an assistant message in the database.
    
    Args:
        db: Database session
        conversation_id: ID of the conversation
        content: Message content
        tool_calls: Optional list of tool calls made by the assistant
        
    Returns:
        The created Message object
    """
    metadata = {"tool_calls": tool_calls} if tool_calls else None
    
    message = Message(
        conversation_id=conversation_id,
        role='assistant',
        content=content,
        metadata_json=str(metadata) if metadata else None
    )
    
    db.add(message)
    db.commit()
    db.refresh(message)
    
    return message


def get_conversation_messages(
    db: Session, 
    conversation_id: str
) -> List[Message]:
    """
    Retrieve all messages for a conversation.
    
    Args:
        db: Database session
        conversation_id: ID of the conversation
        
    Returns:
        List of Message objects in chronological order
    """
    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.timestamp.asc())
        .all()
    )
    
    return messages


def create_conversation(
    db: Session,
    user_id: str,
    title: Optional[str] = None
) -> Conversation:
    """
    Create a new conversation in the database.
    
    Args:
        db: Database session
        user_id: ID of the user creating the conversation
        title: Optional title for the conversation
        
    Returns:
        The created Conversation object
    """
    conversation = Conversation(
        user_id=user_id,
        title=title or "New Conversation"
    )
    
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    
    return conversation


def get_or_create_conversation(
    db: Session,
    user_id: str,
    conversation_id: Optional[str] = None
) -> Conversation:
    """
    Get an existing conversation or create a new one if it doesn't exist.
    
    Args:
        db: Database session
        user_id: ID of the user
        conversation_id: Optional conversation ID (if None, creates a new one)
        
    Returns:
        The Conversation object
    """
    if conversation_id:
        # Try to get existing conversation
        conversation = (
            db.query(Conversation)
            .filter(Conversation.id == conversation_id, Conversation.user_id == user_id)
            .first()
        )
        
        if conversation:
            return conversation
    
    # Create a new conversation
    return create_conversation(db, user_id)