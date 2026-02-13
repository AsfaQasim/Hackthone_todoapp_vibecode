"""Authentication middleware for the AI Chatbot with MCP application."""

from fastapi import Request, status
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

def add_cors_headers(response):
    """Add CORS headers to response."""
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response

async def auth_middleware(request: Request, call_next):
    """Middleware to handle authentication for all requests."""
    # Allow OPTIONS requests (CORS preflight) to pass through without auth
    if request.method == "OPTIONS":
        response = await call_next(request)
        return response
    
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
        response = JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Not authenticated"}
        )
        return add_cors_headers(response)
    
    # Extract and verify token
    token = auth_header.split(" ")[1]
    try:
        # Decode the JWT token
        import jwt
        from src.config import settings
        
        payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"])
        logger.info(f"Token decoded successfully: {payload}")
        
        # Store user info in request state for route handlers
        request.state.user = {
            "user_id": payload.get("sub") or payload.get("userId") or payload.get("user_id"),
            "email": payload.get("email"),
            "name": payload.get("name")
        }
        logger.info(f"✅ Auth successful for user: {payload.get('email')}")
    except jwt.ExpiredSignatureError:
        logger.error("Token has expired")
        response = JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Token has expired"}
        )
        return add_cors_headers(response)
    except jwt.InvalidTokenError as e:
        logger.error(f"Invalid token: {e}")
        response = JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid or expired token"}
        )
        return add_cors_headers(response)
    except Exception as e:
        logger.error(f"Token verification failed: {e}")
        response = JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Invalid or expired token"}
        )
        return add_cors_headers(response)

    response = await call_next(request)
    return response
