"""Conversation service for the AI Chatbot with MCP application."""

from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime
from src.models.base_models import Conversation, Message, User, MessageRole


class ConversationService:
    """Service for managing conversations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_conversation(self, user: User, title: Optional[str] = None) -> Conversation:
        """
        Create a new conversation for the user.
        """
        conversation = Conversation(
            user_id=user.id,
            title=title or "New Conversation"
        )
        
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        
        return conversation
    
    def get_user_conversations(self, user: User) -> List[Conversation]:
        """
        Get all conversations for a user.
        """
        stmt = select(Conversation).where(Conversation.user_id == user.id).order_by(Conversation.created_at.desc())
        return self.db.exec(stmt).all()
    
    def get_conversation_by_id(self, user: User, conversation_id: str) -> Optional[Conversation]:
        """
        Get a specific conversation by ID for the user.
        """
        stmt = select(Conversation).where(Conversation.id == conversation_id, Conversation.user_id == user.id)
        return self.db.exec(stmt).first()
    
    def update_conversation_title(self, user: User, conversation_id: str, title: str) -> Optional[Conversation]:
        """
        Update a conversation's title.
        """
        conversation = self.get_conversation_by_id(user, conversation_id)
        if not conversation:
            return None
        
        conversation.title = title
        self.db.commit()
        self.db.refresh(conversation)
        
        return conversation
    
    def delete_conversation(self, user: User, conversation_id: str) -> bool:
        """
        Delete a conversation and all its messages.
        """
        conversation = self.get_conversation_by_id(user, conversation_id)
        if not conversation:
            return False
        
        # Messages are cascaded automatically if configured correctly, 
        # but to be sure/explicit or if cascade isn't set on DB level:
        # SQLModel relationships with cascade should handle it ideally.
        # But here we explicitly delete them if needed. 
        # Actually with standard relationship cascade="all, delete-orphan", deleting conversation deletes messages.
        
        self.db.delete(conversation)
        self.db.commit()
        
        return True
    
    def get_conversation_messages(self, user: User, conversation_id: str) -> List[Message]:
        """
        Get all messages for a specific conversation.
        """
        # First verify the user owns the conversation
        conversation = self.get_conversation_by_id(user, conversation_id)
        if not conversation:
            return []
        
        stmt = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.timestamp.asc())
        return self.db.exec(stmt).all()
    
    def add_message_to_conversation(
        self, 
        user: User, 
        conversation_id: str, 
        role: str, 
        content: str, 
        metadata: Optional[dict] = None
    ) -> Optional[Message]:
        """
        Add a message to a conversation.
        """
        # Verify the user owns the conversation
        conversation = self.get_conversation_by_id(user, conversation_id)
        if not conversation:
            return None
        
        message = Message(
            conversation_id=conversation_id,
            role=MessageRole(role),
            content=content,
            metadata_json=str(metadata) if metadata else None
        )
        
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        
        return message