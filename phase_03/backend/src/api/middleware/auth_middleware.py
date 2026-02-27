"""Authentication middleware for the AI Chatbot with MCP application."""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from src.services.auth_service import verify_token
import logging

logger = logging.getLogger(__name__)

async def auth_middleware(request: Request, call_next):
    """Middleware to handle authentication for all requests."""
    print(f"\n{'='*60}")
    print(f"🔐 AUTH MIDDLEWARE - Path: {request.url.path}")
    print(f"{'='*60}")
    
    # Skip authentication for health check and public endpoints ONLY
    public_paths = [
        "/", "/health", "/docs", "/redoc", "/openapi.json", "/favicon.ico", "/favicon.png",
        "/login", "/register", "/signup"
    ]

    # Check if path EXACTLY matches or starts with public paths
    is_public = False
    for public_path in public_paths:
        if request.url.path == public_path or (public_path != "/" and request.url.path.startswith(public_path)):
            is_public = True
            break
    
    print(f"Is public path: {is_public}")
    print(f"Public paths checked: {public_paths}")

    # Log the request path and whether it's public
    logger.info(f"Auth middleware: Path={request.url.path}, is_public={is_public}")

    if is_public:
        print(f"✅ Skipping auth for public endpoint")
        logger.info(f"Skipping auth for public endpoint: {request.url.path}")
        response = await call_next(request)
        return response

    # For non-public paths, check if authentication is provided
    # Extract token from Authorization header
    auth_header = request.headers.get("Authorization")
    
    print(f"Authorization header present: {bool(auth_header)}")
    if auth_header:
        print(f"Authorization header (first 30 chars): {auth_header[:30]}...")
    else:
        print(f"❌ NO AUTHORIZATION HEADER FOUND!")
        print(f"All headers: {list(request.headers.keys())}")
    
    logger.info(f"Auth middleware: Checking auth for {request.url.path}")
    logger.info(f"Auth header present: {bool(auth_header)}")
    if auth_header:
        logger.info(f"Auth header value (first 30 chars): {auth_header[:30]}...")

    if not auth_header or not auth_header.startswith("Bearer "):
        print(f"❌ Returning 401 - Not authenticated")
        logger.warning(f"No valid auth header for protected endpoint {request.url.path}")
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
        logger.error(f"HTTP Exception in token verification: {e.detail}")
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