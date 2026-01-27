"""Authentication middleware for the AI Chatbot with MCP application."""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from src.services.auth_service import verify_token
import logging

logger = logging.getLogger(__name__)

async def auth_middleware(request: Request, call_next):
    """Middleware to handle authentication for all requests."""
    # Skip authentication for health check and public endpoints
    public_paths = [
        "/health", "/docs", "/redoc", "/openapi.json",
        "/api/login", "/api/register", "/api/signup",
        "/api/auth/login", "/api/auth/register", "/api/auth/signup",
        "/login", "/register", "/signup", "/auth/login", "/auth/register", "/auth/signup"
    ]

    # Check if this is a chat endpoint that should be handled by route-specific auth
    is_chat_endpoint = request.url.path.startswith("/api/") and "/chat/" in request.url.path

    # Also check for paths that start with auth patterns
    is_public = any(request.url.path.startswith(path) for path in public_paths)

    if is_public or is_chat_endpoint:
        response = await call_next(request)
        return response

    # For non-public paths, check if authentication is provided
    # Extract token from Authorization header
    auth_header = request.headers.get("Authorization")
    print(f"AUTH HEADER RECEIVE 👉 {auth_header}")  # Debug log

    if not auth_header or not auth_header.startswith("Bearer "):
        # If no token is provided, return 401
        # But note: some routes may handle authentication differently
        # so we'll let them override this if needed
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
        logger.error(f"Token verification failed for token: {token[:10]}...")
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