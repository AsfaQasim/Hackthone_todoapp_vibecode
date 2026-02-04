from fastapi import APIRouter, Depends, HTTPException, status, Header
from pydantic import BaseModel
from typing import Optional
from src.services.auth_service import create_access_token, get_current_user, verify_token
from src.db import get_db
import uuid


router = APIRouter()


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
    # For this implementation, we'll simulate a successful login
    # and return a JWT token that the backend can verify
    user_id = str(uuid.uuid4())
    user_data = {
        "sub": user_id,
        "email": login_request.email,
        "user_email": login_request.email,
        "name": login_request.email.split('@')[0]
    }

    token = create_access_token(user_data)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/register", response_model=TokenResponse)
def register(register_request: RegisterRequest):
    """
    Register endpoint that would create a new user in the database
    """
    user_id = str(uuid.uuid4())
    user_data = {
        "sub": user_id,
        "email": register_request.email,
        "user_email": register_request.email,
        "name": register_request.name or register_request.email.split('@')[0]
    }

    token = create_access_token(user_data)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/logout")
def logout():
    """
    Logout endpoint
    """
    return {"message": "Successfully logged out"}


@router.get("/session")
def get_session(current_user=Depends(get_current_user)):
    """
    Get current user session information
    """
    # current_user is a SQLModel User object
    return {
        "user": {
            "id": str(current_user.id),
            "email": current_user.email
        },
        "session": {
            "valid": True
        }
    }


@router.get("/verify-token")
def verify_token_endpoint(authorization: str = Header(None)):
    """
    Verify a JWT token and return user information
    """
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    token = authorization.split(" ")[1]
    
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(token, exception)

    return {
        "id": token_data.user_id,
        "email": token_data.email,
        "name": token_data.email.split('@')[0]
    }