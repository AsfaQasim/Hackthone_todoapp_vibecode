"""Authentication middleware for the AI Chatbot with MCP application."""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from src.services.auth_service import verify_token
import logging

logger = logging.getLogger(__name__)

async def auth_middleware(request: Request, call_next):
    """Middleware to handle authentication for all requests."""
    # Skip authentication for health check and certain public endpoints
    if request.url.path in ["/health", "/docs", "/redoc", "/openapi.json"]:
        response = await call_next(request)
        return response

    # Extract token from Authorization header
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Not authenticated"}
        )

    token = auth_header.split(" ")[1]

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token_data = verify_token(token, credentials_exception)
        # Set both current_user and user for backward compatibility
        request.state.current_user = token_data
        request.state.user = {
            "user_id": token_data.user_id,
            "email": token_data.email
        }
    except HTTPException:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid authentication credentials"}
        )
    except Exception as e:
        # Catch any other exceptions to prevent raw tracebacks
        logger.error(f"Unexpected error in auth middleware: {e}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Authentication error"}
        )

    response = await call_next(request)
    return response