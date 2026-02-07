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
        "/", "/health", "/docs", "/redoc", "/openapi.json", "/favicon.ico", "/favicon.png",
        "/api/login", "/api/register", "/api/signup",
        "/api/auth/login", "/api/auth/register", "/api/auth/signup",
        "/login", "/register", "/signup", "/auth/login", "/auth/register", "/auth/signup",
        "/api/my-tasks"  # Temporary: Allow tasks endpoint without auth
    ]

    # Also check for paths that start with auth patterns or contain specific patterns
    is_public = any(request.url.path.startswith(path) for path in public_paths)
    
    # Temporary: Allow /api/{user_id}/tasks without auth
    if "/tasks" in request.url.path:
        is_public = True

    # Log the request path and whether it's public
    logger.info(f"Auth middleware: Path={request.url.path}, is_public={is_public}")

    if is_public:
        logger.info(f"Skipping auth for public endpoint: {request.url.path}")
        response = await call_next(request)
        return response

    # For non-public paths, check if authentication is provided
    # Extract token from Authorization header
    auth_header = request.headers.get("Authorization")
    logger.info(f"Auth header received: {auth_header}")  # Detailed log

    if not auth_header or not auth_header.startswith("Bearer "):
        logger.warning(f"No valid auth header for protected endpoint {request.url.path}")
        # If no token is provided, return 401
        # But note: some routes may handle authentication differently
        # so we'll let them override this if needed
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Not authenticated"}
        )

    token = auth_header.split(" ")[1]
    logger.info(f"Token received for verification: {token[:15]}...")  # Log token start

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        token_data = verify_token(token, credentials_exception)
        logger.info(f"Token verified successfully for user: {token_data.user_id}")
        # Set both current_user and user for backward compatibility
        request.state.current_user = token_data
        request.state.user = {
            "user_id": token_data.user_id,
            "email": token_data.email
        }
    except HTTPException as e:
        logger.error(f"HTTP Exception in token verification for token {token[:15]}...: {e}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid authentication credentials"}
        )
    except Exception as e:
        # Catch any other exceptions to prevent raw tracebacks
        logger.error(f"Unexpected error in auth middleware for token {token[:15]}...: {e}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Authentication error"}
        )

    response = await call_next(request)
    return response