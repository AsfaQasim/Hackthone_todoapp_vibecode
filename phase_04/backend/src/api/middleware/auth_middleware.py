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
    ]

    # Also check for paths that start with auth patterns or contain specific patterns
    is_public = any(request.url.path.startswith(path) for path in public_paths)
    
    # Chat and tasks endpoints need auth processing
    needs_auth_processing = "/tasks" in request.url.path or "/chat" in request.url.path

    # Log the request path and whether it's public
    logger.info(f"Auth middleware: Path={request.url.path}, is_public={is_public}, needs_auth={needs_auth_processing}")

    if is_public and not needs_auth_processing:
        logger.info(f"Skipping auth for public endpoint: {request.url.path}")
        response = await call_next(request)
        return response

    # For endpoints that need auth processing (tasks, chat) or non-public paths
    # Extract token from Authorization header
    auth_header = request.headers.get("Authorization")
    logger.info(f"Auth header received: {auth_header[:20] if auth_header else 'None'}...")

    if not auth_header or not auth_header.startswith("Bearer "):
        logger.warning(f"No valid auth header for protected endpoint {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Not authenticated"}
        )
    
    # Extract and verify token
    token = auth_header.split(" ")[1]
    try:
        payload = verify_token(token)
        # Store user info in request state for route handlers
        request.state.user = {
            "user_id": payload.get("sub"),
            "email": payload.get("email"),
            "name": payload.get("name")
        }
        logger.info(f"✅ Auth successful for user: {payload.get('email')}")
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid or expired token"}
        )

    response = await call_next(request)
    return response
