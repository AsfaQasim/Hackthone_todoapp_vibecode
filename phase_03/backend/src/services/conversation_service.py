"""Conversation service for the AI Chatbot with MCP application."""

from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from ..models.conversation import Conversation
from ..models.message import Message
from ..models.user import User


class ConversationService:
    """Service for managing conversations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_conversation(self, user: User, title: Optional[str] = None) -> Conversation:
        """
        Create a new conversation for the user.
        
        Args:
            user: The user creating the conversation
            title: Optional title for the conversation
            
        Returns:
            The created Conversation object
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
        
        Args:
            user: The user whose conversations to retrieve
            
        Returns:
            List of Conversation objects
        """
        return (
            self.db.query(Conversation)
            .filter(Conversation.user_id == user.id)
            .order_by(Conversation.created_at.desc())
            .all()
        )
    
    def get_conversation_by_id(self, user: User, conversation_id: str) -> Optional[Conversation]:
        """
        Get a specific conversation by ID for the user.
        
        Args:
            user: The user requesting the conversation
            conversation_id: The ID of the conversation to retrieve
            
        Returns:
            The Conversation object if found and owned by the user, None otherwise
        """
        conversation = (
            self.db.query(Conversation)
            .filter(Conversation.id == conversation_id, Conversation.user_id == user.id)
            .first()
        )
        return conversation
    
    def update_conversation_title(self, user: User, conversation_id: str, title: str) -> Optional[Conversation]:
        """
        Update a conversation's title.
        
        Args:
            user: The user updating the conversation
            conversation_id: The ID of the conversation to update
            title: The new title
            
        Returns:
            The updated Conversation object if successful, None if not found or not owned by user
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
        
        Args:
            user: The user deleting the conversation
            conversation_id: The ID of the conversation to delete
            
        Returns:
            True if deletion was successful, False otherwise
        """
        conversation = self.get_conversation_by_id(user, conversation_id)
        if not conversation:
            return False
        
        # Delete all messages in the conversation first
        self.db.query(Message).filter(Message.conversation_id == conversation_id).delete()
        
        # Then delete the conversation
        self.db.delete(conversation)
        self.db.commit()
        
        return True
    
    def get_conversation_messages(self, user: User, conversation_id: str) -> List[Message]:
        """
        Get all messages for a specific conversation.
        
        Args:
            user: The user requesting the messages
            conversation_id: The ID of the conversation
            
        Returns:
            List of Message objects in chronological order
        """
        # First verify the user owns the conversation
        conversation = self.get_conversation_by_id(user, conversation_id)
        if not conversation:
            return []
        
        return (
            self.db.query(Message)
            .filter(Message.conversation_id == conversation_id)
            .order_by(Message.timestamp.asc())
            .all()
        )
    
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
        
        Args:
            user: The user adding the message
            conversation_id: The ID of the conversation
            role: The role of the message ('user' or 'assistant')
            content: The message content
            metadata: Optional metadata for the message
            
        Returns:
            The created Message object if successful, None if conversation not found or not owned by user
        """
        # Verify the user owns the conversation
        conversation = self.get_conversation_by_id(user, conversation_id)
        if not conversation:
            return None
        
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            metadata_json=str(metadata) if metadata else None
        )
        
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        
        return message