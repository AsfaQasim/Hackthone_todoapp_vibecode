from fastapi import HTTPException, status, Request
from jose import JWTError, jwt
from pydantic import BaseModel
from typing import Optional
import os
from datetime import datetime
from functools import wraps

# JWT configuration
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "fallback_dev_secret_for_testing_only")
ALGORITHM = "HS256"

class TokenData(BaseModel):
    user_id: str
    email: str
    exp: int

def verify_jwt_token(token: str) -> Optional[TokenData]:
    """
    Verify JWT token and return user data
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        email: str = payload.get("email")
        exp: int = payload.get("exp")
        
        if user_id is None or email is None or exp is None:
            return None
            
        # Check if token is expired
        if datetime.utcnow().timestamp() > exp:
            return None
            
        token_data = TokenData(user_id=user_id, email=email, exp=exp)
        return token_data
    except JWTError:
        return None

def get_token_from_header(authorization: str) -> str:
    """
    Extract token from Authorization header
    Expected format: "Bearer <token>"
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication scheme",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return token
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer"},
        )

def require_auth(request: Request) -> TokenData:
    """
    Middleware function to require authentication
    Extracts and verifies JWT token from request
    """
    auth_header = request.headers.get("Authorization")
    token = get_token_from_header(auth_header)
    
    token_data = verify_jwt_token(token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return token_data