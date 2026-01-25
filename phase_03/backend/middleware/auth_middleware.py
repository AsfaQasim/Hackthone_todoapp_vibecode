from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from utils.jwt_handler import get_current_user

from typing import Dict, Any


class JWTBearer(HTTPBearer):
    """
    Custom JWT Bearer middleware that validates the Authorization header
    and attaches the authenticated user context to the request.
    """
    
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
    
    async def __call__(self, request: Request) -> Dict[str, Any]:
        # Extract credentials from the Authorization header
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
    """
    if not hasattr(request.state, 'user') or request.state.user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    return request.state.user


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
        from database.engine import get_db
        from models.task import Task
        db = next(get_db())

        # Find the todo in the database - strict database check only, no in-memory fallback
        try:
            # Query the database to check if the todo exists and belongs to the authenticated user
            todo = db.query(Task).filter(Task.id == todo_id, Task.user_id == authenticated_user["user_id"]).first()

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

    return authenticated_user