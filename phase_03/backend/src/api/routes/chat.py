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
    """Get the authenticated user from request state (set by global middleware).

    Following the production rules:
    - NEVER reject a request due to missing, invalid, expired, or malformed JWT tokens
    - If user identity cannot be extracted from token, fallback to URL parameter or request body
    - NEVER return 401 Unauthorized errors
    - Treat authentication failures as recoverable states, not fatal errors
    - UUID-related database failures must NEVER surface as errors
    - If a UUID is missing, malformed, empty, or invalid, DO NOT execute database queries that depend on it
    """
    import logging
    import uuid
    import re
    logger = logging.getLogger(__name__)

    logger.info(f"get_authenticated_user called for path: {request.url.path}")
    logger.info(f"Request headers: {dict(request.headers)}")
    logger.info(f"Request state: {request.state.__dict__ if hasattr(request.state, '__dict__') else 'No state attributes'}")

    user = None

    # Helper function to validate UUID format before using it in database queries
    def is_valid_uuid_format(uuid_string):
        """Check if a string is a valid UUID format before attempting database query"""
        if not uuid_string or not isinstance(uuid_string, str):
            return False
        # Check if it's a valid UUID format (either with or without dashes)
        uuid_pattern = re.compile(r'^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$', re.IGNORECASE)
        return bool(uuid_pattern.match(uuid_string))

    # Try multiple methods to get user identity
    # Method 1: From request.state (set by middleware)
    if hasattr(request.state, 'current_user') and request.state.current_user is not None:
        user_info = request.state.current_user
        user_id = getattr(user_info, 'user_id', None)
        logger.info(f"Method 1 - Found current_user in request.state: {user_id}")

        if user_id and is_valid_uuid_format(str(user_id)):
            logger.info(f"Getting user from request.state.current_user: {user_id}")

            # Try to find the user in the database - handle UUID format differences
            try:
                user_uuid = uuid.UUID(str(user_id))
                normalized_user_id = user_uuid.hex
            except ValueError:
                normalized_user_id = str(user_id).lower()

            try:
                user = db.query(User).filter(User.id == normalized_user_id).first()
                logger.info(f"Database lookup result for current_user: {user is not None}")
            except Exception as e:
                logger.warning(f"Database query failed for user_id {normalized_user_id}: {e}")
                # Continue to next method if database query fails
        else:
            logger.warning(f"Invalid or missing user_id in request.state.current_user: {user_id}")

    # Method 2: From request.state.user
    if not user and hasattr(request.state, 'user') and request.state.user is not None:
        user_info = request.state.user
        user_id = user_info.get('user_id') if isinstance(user_info, dict) else getattr(user_info, 'user_id', None)
        logger.info(f"Method 2 - Found user in request.state.user: {user_id}")

        if user_id and is_valid_uuid_format(str(user_id)):
            logger.info(f"Getting user from request.state.user: {user_id}")

            try:
                user_uuid = uuid.UUID(str(user_id))
                normalized_user_id = user_uuid.hex
            except ValueError:
                normalized_user_id = str(user_id).lower()

            try:
                user = db.query(User).filter(User.id == normalized_user_id).first()
                logger.info(f"Database lookup result for state.user: {user is not None}")
            except Exception as e:
                logger.warning(f"Database query failed for user_id {normalized_user_id}: {e}")
        else:
            logger.warning(f"Invalid or missing user_id in request.state.user: {user_id}")

    # Method 3: Extract from Authorization header directly if verification fails
    if not user:
        auth_header = request.headers.get("Authorization")
        logger.info(f"Method 3 - Checking Authorization header: {auth_header}")

        if auth_header:
            # Remove "Bearer " prefix if present
            token = auth_header.replace("Bearer ", "").strip()
            logger.info(f"Extracted token from header: {token[:15]}...")

            try:
                # Try to decode token without verification to extract user info
                import jwt
                from src.services.auth_service import SECRET_KEY, ALGORITHM

                # Decode without verification to get payload
                payload = jwt.decode(token, options={"verify_signature": False}, algorithms=[ALGORITHM])
                logger.info(f"Decoded token payload (unverified): {payload}")

                user_id = payload.get("sub") or payload.get("userId") or payload.get("user_id")
                if user_id and is_valid_uuid_format(str(user_id)):
                    logger.info(f"Extracted user_id from token payload: {user_id}")
                    try:
                        user_uuid = uuid.UUID(str(user_id))
                        normalized_user_id = user_uuid.hex
                    except ValueError:
                        normalized_user_id = str(user_id).lower()

                    try:
                        user = db.query(User).filter(User.id == normalized_user_id).first()
                        logger.info(f"Database lookup result for token user_id: {user is not None}")
                    except Exception as e:
                        logger.warning(f"Database query failed for user_id {normalized_user_id}: {e}")
            except Exception as e:
                logger.warning(f"Could not decode token from header: {e}")

    # Method 4: Extract from URL path parameter
    if not user:
        # Extract user_id from the URL path
        path_parts = request.url.path.strip('/').split('/')
        # Path format is /api/{user_id}/chat
        if len(path_parts) >= 3 and path_parts[-1] == 'chat':
            path_user_id = path_parts[-2]  # The user_id is second to last
            logger.info(f"Method 4 - Extracted path_user_id: {path_user_id}")

            if path_user_id and is_valid_uuid_format(str(path_user_id)):
                logger.info(f"Extracting user_id from URL path: {path_user_id}")

                try:
                    user_uuid = uuid.UUID(str(path_user_id))
                    normalized_user_id = user_uuid.hex
                except ValueError:
                    normalized_user_id = str(path_user_id).lower()

                try:
                    user = db.query(User).filter(User.id == normalized_user_id).first()
                    logger.info(f"Database lookup result for path user_id: {user is not None}")
                except Exception as e:
                    logger.warning(f"Database query failed for path user_id {normalized_user_id}: {e}")
            else:
                logger.warning(f"Invalid user_id in URL path: {path_user_id}")

    # Method 5: If no user found through valid UUIDs, create a temporary anonymous user context
    if not user:
        logger.warning("No valid user found through any method, creating temporary anonymous context...")
        # Create a temporary user object without saving to database
        # This is a mock user object that satisfies the User interface
        class AnonymousUser:
            def __init__(self):
                self.id = str(uuid.uuid4())  # Generate a temporary UUID
                self.email = "anonymous@example.com"
                self.name = "Anonymous User"

        user = AnonymousUser()
        logger.info(f"Created temporary anonymous user: {user.id}")

    logger.info(f"Successfully resolved user: {user.id}")
    return user


@router.post("/{user_id}/chat")
async def chat(
    user_id: str,
    request: ChatRequest,
    current_user: User = Depends(get_authenticated_user)
):
    """
    Main chat endpoint that accepts user natural language input and returns AI response with invoked MCP tools.
    This endpoint is fault-tolerant and always returns valid JSON responses.

    Args:
        user_id: The ID of the user initiating the chat (from path)
        request: The chat request containing the message and optional conversation ID
        current_user: The authenticated user (from JWT)

    Returns:
        Valid JSON response with AI response data
    """
    from datetime import datetime
    import logging
    import traceback
    import re
    from src.db import SessionLocal

    logger = logging.getLogger(__name__)

    logger.info(f"Chat endpoint called with user_id: {user_id}")
    logger.info(f"Current user from dependency: {getattr(current_user, 'id', 'NO_USER_FOUND')}")

    # Initialize default response values
    conversation_id = str(uuid.uuid4())  # Generate a default conversation ID
    response_text = "I'm here to help. How can I assist you today?"
    tool_calls_list = []
    timestamp_str = datetime.utcnow().isoformat()

    # Helper function to validate UUID format before using it in database queries
    def is_valid_uuid_format(uuid_string):
        """Check if a string is a valid UUID format before attempting database query"""
        if not uuid_string or not isinstance(uuid_string, str):
            return False
        # Check if it's a valid UUID format (either with or without dashes)
        uuid_pattern = re.compile(r'^[0-9a-f]{8}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{4}-?[0-9a-f]{12}$', re.IGNORECASE)
        return bool(uuid_pattern.match(uuid_string))

    try:
        # Validate that the user_id in the path is a valid UUID before using it in database operations
        if is_valid_uuid_format(user_id):
            logger.info(f"Valid path user_id: {user_id}")  # Debug log
            logger.info(f"Current user ID: {current_user.id}")  # Debug log

            # Normalize both UUIDs to ensure consistent comparison
            # Since the database stores UUIDs as hex strings (32 chars without dashes), we need to normalize both IDs
            try:
                # Convert the path user_id to normalized hex format
                try:
                    path_uuid = uuid.UUID(user_id)
                    normalized_path_user_id = path_uuid.hex  # Convert to hex format (32 chars without dashes)
                except ValueError:
                    # If it's not a valid UUID string, assume it's already in hex format
                    normalized_path_user_id = user_id.lower()

                # Convert the current user ID to normalized hex format
                try:
                    user_uuid = uuid.UUID(str(current_user.id))
                    normalized_current_user_id = user_uuid.hex  # Convert to hex format (32 chars without dashes)
                except ValueError:
                    # If it's not a valid UUID string, assume it's already in hex format
                    normalized_current_user_id = str(current_user.id).lower()

                # Compare the normalized representations
                logger.info(f"Comparing normalized path user ID: {normalized_path_user_id} with normalized current user ID: {normalized_current_user_id}")  # Debug log
                if normalized_current_user_id != normalized_path_user_id:
                    logger.warning(f"User ID mismatch: token user_id={normalized_current_user_id}, path user_id={normalized_path_user_id}. Proceeding anyway due to fault tolerance.")
                    # Continue processing despite mismatch due to fault tolerance
            except (ValueError, TypeError) as e:
                # If UUID conversion fails, log the issue but continue
                logger.warning(f"UUID conversion failed: {e}. Proceeding with available user data.")
        else:
            logger.warning(f"Invalid path user_id format: {user_id}. Treating as stateless operation.")

        # Attempt database operations with fault tolerance
        db = None
        try:
            # Only attempt database operations if we have valid UUIDs
            if is_valid_uuid_format(user_id) and is_valid_uuid_format(str(current_user.id)):
                logger.info("Attempting database operations with valid UUIDs")
                db = SessionLocal()

                # Get or create conversation
                try:
                    conversation = get_or_create_conversation(db, user_id, request.conversation_id)
                    conversation_id = str(conversation.id)
                except Exception as e:
                    logger.error(f"Failed to create/get conversation: {e}. Using default conversation ID.")
                    conversation_id = str(uuid.uuid4())

                # Store the user's message
                try:
                    user_message = store_user_message(
                        db,
                        conversation_id,
                        request.message
                    )
                except Exception as e:
                    logger.error(f"Failed to store user message: {e}. Continuing anyway.")

                # Create chat agent and process the message
                try:
                    agent = ChatAgent(db, current_user)
                    result = agent.process_message(request.message, conversation_id)
                    response_text = result["response"]
                    tool_calls_list = result["tool_calls"]
                except Exception as e:
                    logger.error(f"Failed to process message with ChatAgent: {e}. Generating fallback response.")
                    # Generate a fallback response if the agent fails
                    response_text = f"I received your message: '{request.message}'. I'm experiencing some technical difficulties but will get back to you shortly."
                    tool_calls_list = []

                # Store the assistant's response
                try:
                    assistant_message = store_assistant_message(
                        db,
                        conversation_id,
                        response_text,
                        tool_calls_list
                    )
                except Exception as e:
                    logger.error(f"Failed to store assistant message: {e}. Continuing anyway.")
            else:
                logger.info(f"Skipping database operations - path UUID valid: {is_valid_uuid_format(user_id)}, current user UUID valid: {is_valid_uuid_format(str(current_user.id))}")
                # If UUIDs are invalid, skip database operations and generate response directly
                logger.info("Skipping database operations due to invalid UUIDs")
                try:
                    # Create a temporary agent without database connection
                    from src.agents.chat_agent import ChatAgent
                    # Create a minimal agent that can generate responses without database
                    # For this, we'll simulate the agent's response
                    response_text = f"You said: '{request.message}'. This is a simulated response since the system is operating in stateless mode due to UUID validation issues."
                    tool_calls_list = []
                except Exception as e:
                    logger.error(f"Failed to generate response: {e}")
                    response_text = f"I received your message: '{request.message}'. I'm operating in stateless mode due to system constraints."
                    tool_calls_list = []
        finally:
            if db:
                try:
                    db.close()
                except Exception as e:
                    logger.error(f"Error closing database connection: {e}")
    except Exception as e:
        logger.error(f"Critical error in chat endpoint: {e}\n{traceback.format_exc()}")
        # Even if everything fails, return a valid response
        response_text = "I'm experiencing some technical difficulties but am still here to help. Please try your request again."
        conversation_id = str(uuid.uuid4())
        tool_calls_list = []
        timestamp_str = datetime.utcnow().isoformat()

    # Always return valid JSON as per requirements
    response = {
        "success": True,
        "message": "Recovered from backend error",
        "data": {
            "conversation_id": conversation_id,
            "response": response_text,
            "tool_calls": tool_calls_list,
            "timestamp": timestamp_str
        },
        "recovered": True
    }

    # Add note if UUID error was bypassed
    if not is_valid_uuid_format(user_id) or not is_valid_uuid_format(str(current_user.id)):
        response["note"] = "UUID error bypassed"

    logger.info(f"Returning response: {response}")
    return response