from fastapi import APIRouter, Depends, HTTPException, status, Header
from pydantic import BaseModel
from typing import Optional
from sqlmodel import Session
from src.services.auth_service import create_access_token, get_current_user, verify_token
from src.db import get_db
import uuid
import logging
import traceback


router = APIRouter()
logger = logging.getLogger(__name__)


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
    user_id: Optional[str] = None
    token: Optional[str] = None  # Alias for access_token for frontend compatibility


@router.post("/login", response_model=TokenResponse)
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    """
    Login endpoint that validates credentials against the database
    """
    try:
        from src.models.base_models import User
        
        logger.info(f"=" * 60)
        logger.info(f"🔐 LOGIN REQUEST: {login_request.email}")
        
        # Check if user exists in database
        existing_user = db.query(User).filter(User.email == login_request.email).first()
        
        logger.info(f"📊 Database query result: {existing_user}")
        
        if existing_user:
            # User exists, use their ID
            user_id = str(existing_user.id)
            logger.info(f"✅ Existing user found: {existing_user.email} (ID: {user_id})")
            logger.info(f"🎯 USING EXISTING USER ID: {user_id}")
        else:
            # User doesn't exist, create new user
            import uuid
            user_id = str(uuid.uuid4())
            
            logger.info(f"⚠️  User not found in database, creating new user")
            logger.info(f"🆕 NEW USER ID: {user_id}")
            
            new_user = User(
                id=user_id,
                email=login_request.email,
                name=login_request.email.split('@')[0]
            )
            
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            logger.info(f"✅ New user created: {new_user.email} (ID: {user_id})")
        
        logger.info(f"🔑 Final user_id being returned: {user_id}")
        logger.info(f"=" * 60)
        
        # Create JWT token
        user_data = {
            "sub": user_id,
            "email": login_request.email,
            "user_email": login_request.email,
            "name": login_request.email.split('@')[0]
        }

        token = create_access_token(user_data)
        return {
            "access_token": token,
            "token": token,  # Alias for frontend
            "token_type": "bearer",
            "user_id": user_id
        }
    except Exception as e:
        logger.error(f"Login error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed due to an internal server error"
        )


@router.post("/register", response_model=TokenResponse)
def register(register_request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register endpoint that creates a new user in the database
    """
    try:
        from src.models.base_models import User
        import uuid
        
        # Generate user ID
        user_id = uuid.uuid4()
        
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == register_request.email).first()
        if existing_user:
            logger.info(f"User already exists: {register_request.email}")
            # Return token for existing user
            user_data = {
                "sub": str(existing_user.id),
                "email": existing_user.email,
                "user_email": existing_user.email,
                "name": existing_user.name
            }
            token = create_access_token(user_data)
            return {
                "access_token": token,
                "token": token,  # Alias for frontend
                "token_type": "bearer",
                "user_id": str(existing_user.id)
            }
        
        # Create new user in database
        new_user = User(
            id=user_id,
            email=register_request.email,
            name=register_request.name or register_request.email.split('@')[0]
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        logger.info(f"✅ New user created in database: {new_user.email} (ID: {new_user.id})")
        
        # Create token with the actual user ID from database
        user_data = {
            "sub": str(new_user.id),
            "email": new_user.email,
            "user_email": new_user.email,
            "name": new_user.name
        }

        token = create_access_token(user_data)
        return {
            "access_token": token,
            "token": token,  # Alias for frontend
            "token_type": "bearer",
            "user_id": str(new_user.id)
        }
    except Exception as e:
        logger.error(f"Registration error: {e}")
        logger.error(traceback.format_exc())
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed due to an internal server error"
        )


@router.post("/logout")
def logout():
    """
    Logout endpoint
    """
    try:
        return {"message": "Successfully logged out"}
    except Exception as e:
        logger.error(f"Logout error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout failed due to an internal server error"
        )


@router.get("/session")
def get_session(current_user=Depends(get_current_user)):
    """
    Get current user session information
    """
    try:
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
    except Exception as e:
        logger.error(f"Session error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Session retrieval failed due to an internal server error"
        )


@router.get("/verify-token")
def verify_token_endpoint(authorization: str = Header(None)):
    """
    Verify a JWT token and return user information
    """
    try:
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
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Token verification error: {e}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token verification failed due to an internal server error"
        )