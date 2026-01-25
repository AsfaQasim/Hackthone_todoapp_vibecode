"""Chat endpoint for the AI Chatbot with MCP application."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
import uuid

from ..services.auth_service import get_current_user
from ..models.user import User
from ..db import get_db
from ..agents.chat_agent import ChatAgent
from ..services.message_service import get_or_create_conversation, store_user_message, store_assistant_message
from ..services.conversation_service import ConversationService


router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    """Request model for the chat endpoint."""
    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for the chat endpoint."""
    conversation_id: str
    response: str
    tool_calls: list
    timestamp: str


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Main chat endpoint that accepts user natural language input and returns AI response with invoked MCP tools.
    
    Args:
        user_id: The ID of the user initiating the chat (from path)
        request: The chat request containing the message and optional conversation ID
        current_user: The authenticated user (from JWT)
        db: Database session
        
    Returns:
        ChatResponse containing the AI response and any tool invocations
    """
    from datetime import datetime
    
    # Validate that the user_id in the path matches the user in the JWT
    if str(current_user.id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in token does not match user ID in path"
        )
    
    # Get or create conversation
    conversation = get_or_create_conversation(db, user_id, request.conversation_id)
    conversation_id = str(conversation.id)
    
    # Store the user's message
    user_message = store_user_message(
        db, 
        conversation_id, 
        request.message
    )
    
    # Create chat agent and process the message
    agent = ChatAgent(db, current_user)
    result = agent.process_message(request.message, conversation_id)
    
    # Store the assistant's response
    assistant_message = store_assistant_message(
        db,
        conversation_id,
        result["response"],
        result["tool_calls"]
    )
    
    # Return the response
    return ChatResponse(
        conversation_id=conversation_id,
        response=result["response"],
        tool_calls=result["tool_calls"],
        timestamp=datetime.utcnow().isoformat()
    )