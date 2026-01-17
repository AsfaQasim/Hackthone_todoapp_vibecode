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


def verify_user_owns_resource(request: Request, user_id_in_path: str) -> Dict[str, Any]:
    """
    Dependency to verify that the authenticated user owns the requested resource.
    This enforces user isolation by checking that the user_id in the URL matches
    the authenticated user's ID.
    """
    authenticated_user = verify_user_is_authenticated(request)
    
    # Check if the authenticated user's ID matches the user_id in the path
    if authenticated_user["user_id"] != user_id_in_path:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own resources"
        )
    
    return authenticated_user