from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils.jwt_handler import get_current_user

from typing import Dict, Any


class JWTBearer(HTTPBearer):
    """
    Custom JWT Bearer middleware that validates the Authorization header
    and attaches the authenticated user context to the request.

    Note: When used with the global auth middleware, this will use the
    pre-authenticated user from request.state instead of validating the token again.
    """

    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> Dict[str, Any]:
        # Check if the global middleware has already authenticated the user
        if hasattr(request.state, 'user') and request.state.user is not None:
            # Use the pre-authenticated user from global middleware
            return request.state.user

        # If no pre-authenticated user, fall back to manual token validation
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)

        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication scheme."
                )

            # Verify the token and get user info
            user_info = get_current_user(credentials.credentials)

            # Attach user info to the request object for later use
            request.state.user = user_info

            return user_info
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization token."
            )


def verify_user_is_authenticated(request: Request) -> Dict[str, Any]:
    """
    Dependency to verify that a user is authenticated.
    This can be used to protect API endpoints.
    Works with both global middleware and standalone authentication.
    """
    # Check if global middleware has already authenticated the user
    if hasattr(request.state, 'user') and request.state.user is not None:
        return request.state.user

    # Also check if the current_user was set by the global middleware
    if hasattr(request.state, 'current_user') and request.state.current_user is not None:
        # Convert current_user to the expected format
        return {
            "user_id": request.state.current_user.user_id,
            "email": request.state.current_user.email
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authentication required"
    )


def verify_user_owns_resource(request: Request, user_id_in_path: str = None, todo_id: str = None) -> Dict[str, Any]:
    """
    Dependency to verify that the authenticated user owns the requested resource.
    This enforces user isolation by checking that the user_id in the URL matches
    the authenticated user's ID.

    Args:
        request: The incoming request object
        user_id_in_path: The user ID from the URL path (optional)
        todo_id: The todo ID to check ownership for (optional)
    """
    authenticated_user = verify_user_is_authenticated(request)

    # If a specific user_id is provided in the path, check if it matches the authenticated user
    if user_id_in_path and authenticated_user["user_id"] != user_id_in_path:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own resources"
        )

    # If a todo_id is provided, verify that the authenticated user owns that specific todo
    if todo_id:
        from src.db import SessionLocal
        from src.models.base_models import Task as DBTask
        db = SessionLocal()

        try:
            # Find the todo in the database - strict database check only, no in-memory fallback
            # Query the database to check if the todo exists and belongs to the authenticated user
            todo = db.query(DBTask).filter(DBTask.id == todo_id, DBTask.user_id == authenticated_user["user_id"]).first()

            if not todo:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied: You can only access your own resources"
                )
        except Exception as e:
            # Log the error for debugging but don't expose internal details to the client
            print(f"Database error in verify_user_owns_resource: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Could not verify resource ownership"
            )
        finally:
            db.close()

    return authenticated_user