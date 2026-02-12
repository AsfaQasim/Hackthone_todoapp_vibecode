from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional
from utils.jwt_handler import JWTHandler, get_current_user
from middleware.auth_middleware import JWTBearer
from database.engine import get_db



router = APIRouter()
jwt_handler = JWTHandler()


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: Optional[str] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=TokenResponse)
def login(login_request: LoginRequest):
    """
    Login endpoint that would validate credentials against the database
    In a real implementation, this would verify the user's credentials
    and return a JWT token. Since we're using Better Auth on the frontend,
    this is mainly for compatibility purposes.
    """
    # In a real implementation, you would:
    # 1. Verify the user's credentials against the database
    # 2. Create a JWT token with user information
    # 3. Return the token
    
    # For this implementation, we'll simulate a successful login
    # and return a JWT token that the backend can verify
    user_data = {
        "userId": f"user_{hash(login_request.email)}",  # In reality, get from DB
        "email": login_request.email,
        "name": login_request.name or login_request.email.split('@')[0]
    }
    
    token = jwt_handler.create_access_token(user_data)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", response_model=TokenResponse)
def register(register_request: RegisterRequest):
    """
    Register endpoint that would create a new user in the database
    In a real implementation, this would create a new user record
    and return a JWT token. Since we're using Better Auth on the frontend,
    this is mainly for compatibility purposes.
    """
    # In a real implementation, you would:
    # 1. Create a new user in the database
    # 2. Hash the password
    # 3. Create a JWT token with user information
    # 4. Return the token
    
    # For this implementation, we'll simulate a successful registration
    # and return a JWT token that the backend can verify
    user_data = {
        "userId": f"user_{hash(register_request.email)}",  # In reality, get from DB
        "email": register_request.email,
        "name": register_request.name or register_request.email.split('@')[0]
    }
    
    token = jwt_handler.create_access_token(user_data)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/logout")
def logout():
    """
    Logout endpoint - since we're stateless, this is mostly a client-side operation
    """
    return {"message": "Successfully logged out"}


@router.get("/session", dependencies=[Depends(JWTBearer())])
def get_session(current_user=Depends(get_current_user)):
    """
    Get current user session information
    This endpoint is protected and requires a valid JWT token
    """
    return {
        "user": {
            "id": current_user["user_id"],
            "email": current_user["email"]
        },
        "session": {
            "valid": True,
            "exp": current_user["exp"]
        }
    }