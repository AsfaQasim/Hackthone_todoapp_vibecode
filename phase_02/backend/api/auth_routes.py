from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlmodel import Session
from datetime import timedelta
from utils.db import get_session
from utils.jwt_handler import create_access_token
from models.todo_models import User, UserCreate
from api.user_service import get_user_by_email, create_user_in_db, authenticate_user

router = APIRouter(tags=["auth"])

class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    email: str
    password: str
    name: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    user: dict

@router.post("/api/auth/sign-in/email", response_model=TokenResponse)
async def login(
    login_data: LoginRequest, 
    session: Session = Depends(get_session)
):
    """
    Login endpoint - validates email/password against Neon DB
    """
    user = authenticate_user(session, login_data.email, login_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    # Create access token
    access_token_expires = timedelta(minutes=30)  # Token valid for 30 minutes
    access_token = create_access_token(
        data={"user_id": user.id, "email": user.email},
        expires_delta=access_token_expires
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user={
            "id": user.id,
            "email": user.email,
            "name": user.name or user.email.split('@')[0]
        }
    )

@router.post("/api/auth/sign-up/email", response_model=TokenResponse)
async def signup(
    signup_data: SignupRequest, 
    session: Session = Depends(get_session)
):
    """
    Signup endpoint - creates user with hashed password
    """
    # Check if user already exists
    existing_user = get_user_by_email(session, signup_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists"
        )

    # Create new user - password will be hashed in create_user_in_db
    user_data = UserCreate(
        email=signup_data.email,
        name=signup_data.name,
        password=signup_data.password
    )

    user = create_user_in_db(session, user_data)

    # Create access token
    access_token_expires = timedelta(minutes=30)  # Token valid for 30 minutes
    access_token = create_access_token(
        data={"user_id": user.id, "email": user.email},
        expires_delta=access_token_expires
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        user={
            "id": user.id,
            "email": user.email,
            "name": user.name or user.email.split('@')[0]
        }
    )

@router.post("/api/auth/sign-out")
async def logout():
    """
    Logout endpoint - invalidate session
    """
    return {"success": True}