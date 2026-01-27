"""Chat endpoint for the AI Chatbot with MCP application."""

from fastapi import APIRouter, Request, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel
import uuid

from src.models.base_models import User
from src.db import get_db
from src.agents.chat_agent import ChatAgent
from src.services.message_service import get_or_create_conversation, store_user_message, store_assistant_message
from src.services.conversation_service import ConversationService


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


async def get_authenticated_user(request: Request, db: Session = Depends(get_db)):
    """Get the authenticated user from request state (set by global middleware)."""
    import logging
    import uuid
    logger = logging.getLogger(__name__)

    if not hasattr(request.state, 'current_user') or request.state.current_user is None:
        if not hasattr(request.state, 'user') or request.state.user is None:
            logger.error("No authentication data found in request.state")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required"
            )
        # Convert the user format if needed
        user_info = request.state.user
        logger.info(f"Looking up user by ID: {user_info['user_id']}")

        # Try to find the user in the database - handle UUID format differences
        user = db.query(User).filter(User.id == user_info["user_id"]).first()

        # If not found, try converting the user_id to different UUID formats
        if not user:
            try:
                # Try converting to UUID object and back to string to normalize
                user_uuid = uuid.UUID(str(user_info["user_id"]))

                # Try with hex representation (32-char without dashes) - this is how it's stored in DB
                user = db.query(User).filter(User.id == user_uuid.hex).first()

                # If still not found, try with canonical format (with dashes)
                if not user:
                    user = db.query(User).filter(User.id == str(user_uuid)).first()

            except Exception as e:
                logger.error(f"Error converting UUID: {e}")
                pass  # Ignore UUID conversion errors

        if not user:
            # The user ID exists in the token but not in the database
            # This could happen if the user was deleted after token issuance
            logger.error(f"User not found in database: {user_info['user_id']}")
            # Try to handle the case where the user_id might be in a different format
            # Check if it's a UUID string that needs to be converted
            try:
                user_uuid = uuid.UUID(str(user_info["user_id"]))
                # Try to find with both hex and canonical formats
                user = db.query(User).filter(User.id == user_uuid.hex).first()
                if not user:
                    user = db.query(User).filter(User.id == str(user_uuid)).first()
            except Exception:
                pass  # If UUID conversion fails, continue to raise error

        if not user:
            # The user ID exists in the token but not in the database
            logger.error(f"User not found in database: {user_info['user_id']}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account not found"
            )
        logger.info(f"Successfully authenticated user: {user.id}")
        return user
    else:
        # Use the current_user from the new middleware
        logger.info(f"Looking up user by ID: {request.state.current_user.user_id}")

        # Try to find the user in the database - handle UUID format differences
        user = db.query(User).filter(User.id == request.state.current_user.user_id).first()

        # If not found, try converting the user_id to different UUID formats
        if not user:
            try:
                # Try converting to UUID object and back to string to normalize
                user_uuid = uuid.UUID(str(request.state.current_user.user_id))

                # Try with hex representation (32-char without dashes) - this is how it's stored in DB
                user = db.query(User).filter(User.id == user_uuid.hex).first()

                # If still not found, try with canonical format (with dashes)
                if not user:
                    user = db.query(User).filter(User.id == str(user_uuid)).first()

            except Exception as e:
                logger.error(f"Error converting UUID: {e}")
                pass  # Ignore UUID conversion errors

        if not user:
            # The user ID exists in the token but not in the database
            logger.error(f"User not found in database: {request.state.current_user.user_id}")
            # Try to handle the case where the user_id might be in a different format
            # Check if it's a UUID string that needs to be converted
            try:
                user_uuid = uuid.UUID(str(request.state.current_user.user_id))
                # Try to find with both hex and canonical formats
                user = db.query(User).filter(User.id == user_uuid.hex).first()
                if not user:
                    user = db.query(User).filter(User.id == str(user_uuid)).first()
            except Exception:
                pass  # If UUID conversion fails, continue to raise error

        if not user:
            # The user ID exists in the token but not in the database
            logger.error(f"User not found in database: {request.state.current_user.user_id}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User account not found"
            )
        logger.info(f"Successfully authenticated user: {user.id}")
        return user


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    current_user: User = Depends(get_authenticated_user)
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
    import logging

    logger = logging.getLogger(__name__)

    try:
        # Validate that the user_id in the path matches the user in the JWT
        # Handle UUID format differences (canonical vs hex string vs different representations)
        current_user_id_str = str(current_user.id)
        logger.info(f"Path user_id: {user_id}")  # Debug log
        logger.info(f"Current user ID: {current_user_id_str}")  # Debug log

        # Normalize both UUIDs to ensure consistent comparison
        try:
            # Convert the path user_id to UUID object (could be canonical or hex format)
            try:
                path_uuid = uuid.UUID(user_id)
                path_uuid_hex = path_uuid.hex  # Convert to hex format (32 chars without dashes)
            except ValueError:
                # If it's not a valid UUID string, assume it's already in hex format
                path_uuid_hex = user_id

            # Convert the current user ID to UUID object (could be canonical or hex format)
            try:
                user_uuid = uuid.UUID(current_user_id_str)
                user_uuid_hex = user_uuid.hex  # Convert to hex format (32 chars without dashes)
            except ValueError:
                # If it's not a valid UUID string, assume it's already in hex format
                user_uuid_hex = current_user_id_str

            # Compare the hex representations (both should be in the same format now)
            logger.info(f"Comparing path UUID hex: {path_uuid_hex} with user UUID hex: {user_uuid_hex}")  # Debug log
            if user_uuid_hex != path_uuid_hex:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"User ID mismatch: token user_id={user_uuid_hex}, path user_id={path_uuid_hex}"
                )
        except (ValueError, TypeError) as e:
            # If UUID conversion fails, compare as strings but log the issue
            logger.warning(f"UUID conversion failed: {e}")
            if current_user_id_str != user_id:
                logger.warning(f"User ID format issue: current_user_id='{current_user_id_str}', path_user_id='{user_id}'")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"User ID mismatch: {current_user_id_str} != {user_id}"
                )

        # Get the database session
        from src.db import SessionLocal
        db = SessionLocal()
        try:
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
        finally:
            db.close()

        # Return the response
        return ChatResponse(
            conversation_id=conversation_id,
            response=result["response"],
            tool_calls=result["tool_calls"],
            timestamp=datetime.utcnow().isoformat()
        )
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        # Log the error and raise an internal server error
        logger.error(f"Unexpected error in chat endpoint: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request"
        )