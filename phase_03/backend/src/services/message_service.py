"""Message persistence layer for storing user/assistant messages in DB."""

from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from src.models.base_models import Message, Conversation, MessageRole


def store_user_message(
    db: Session, 
    conversation_id: str, 
    content: str, 
    metadata: Optional[dict] = None
) -> Message:
    """
    Store a user message in the database.
    """
    message = Message(
        conversation_id=conversation_id,
        role=MessageRole.USER,
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
    """
    metadata = {"tool_calls": tool_calls} if tool_calls else None
    
    message = Message(
        conversation_id=conversation_id,
        role=MessageRole.ASSISTANT,
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
    """
    stmt = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.timestamp.asc())
    return db.exec(stmt).all()


def create_conversation(
    db: Session,
    user_id: str,
    title: Optional[str] = None
) -> Conversation:
    """
    Create a new conversation in the database.
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
    """
    if conversation_id:
        # Try to get existing conversation
        stmt = select(Conversation).where(Conversation.id == conversation_id, Conversation.user_id == user_id)
        conversation = db.exec(stmt).first()
        
        if conversation:
            return conversation
    
    # Create a new conversation
    return create_conversation(db, user_id)