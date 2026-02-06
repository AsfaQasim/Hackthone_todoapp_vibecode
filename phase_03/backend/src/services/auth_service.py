"""Authentication service with JWT enforcement for the AI Chatbot with MCP application."""

from datetime import datetime, timedelta
from typing import Optional
import jwt
import uuid
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlmodel import Session, select
from src.db import get_db
from src.models.base_models import User
import os
from dotenv import load_dotenv
import logging
import traceback

logger = logging.getLogger(__name__)

load_dotenv()

# JWT configuration
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 24 hours

security = HTTPBearer()

class TokenData(BaseModel):
    user_id: str
    email: str

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a new JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Use config value
    to_encode.update({"exp": expire})

    # Ensure the user ID is available as both "sub" and "userId" for compatibility
    if "user_id" in to_encode and "sub" not in to_encode:
        to_encode["sub"] = to_encode["user_id"]
    if "user_id" in to_encode and "userId" not in to_encode:
        to_encode["userId"] = to_encode["user_id"]

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    logger.info(f"Created access token with payload: {to_encode}")
    return encoded_jwt

def verify_token(token: str, credentials_exception):
    """Verify the JWT token and return the token data."""
    logger.info(f"Verifying token: {token[:15]}... with secret key presence: {bool(SECRET_KEY)}")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info(f"Decoded token payload: {payload}")

        # Try to get user ID from multiple possible fields
        user_id: str = payload.get("sub") or payload.get("userId") or payload.get("user_id")
        email: str = payload.get("email")
        logger.info(f"Extracted user_id: {user_id}, email: {email}")

        if user_id is None or email is None:
            logger.warning(f"Missing user_id or email in token payload")
            raise credentials_exception
        token_data = TokenData(user_id=user_id, email=email)
        logger.info(f"Token verification successful for user: {user_id}")
    except jwt.ImmatureSignatureError:
        logger.error("Token is not yet valid (immature)")
        raise credentials_exception
    except jwt.ExpiredSignatureError:
        logger.error("Token has expired")
        raise credentials_exception
    except jwt.InvalidAlgorithmError:
        logger.error("Token has invalid algorithm")
        raise credentials_exception
    except jwt.InvalidTokenError:
        logger.error("Token is invalid")
        raise credentials_exception
    except jwt.DecodeError:
        logger.error("Token decode error")
        raise credentials_exception
    except Exception as e:
        logger.error(f"Unexpected error during token verification: {e}")
        raise credentials_exception
    return token_data

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """Get the current user based on the JWT token."""
    try:
        logger.info(f"Getting current user with credentials: {credentials.credentials[:15]}...")

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        token_data = verify_token(credentials.credentials, credentials_exception)

        user_id = token_data.user_id
        logger.info(f"Looking up user in DB with ID: {user_id}")

        # Simple direct query first
        try:
            stmt = select(User).where(User.id == user_id)
            user = db.exec(stmt).first()
            logger.info(f"Found user in DB: {user is not None}")
        except Exception as e:
            logger.error(f"Database query error for user_id {user_id}: {e}")
            # Fallback for UUID conversion issues if incoming string format differs
            try:
                uuid_val = uuid.UUID(user_id)
                stmt = select(User).where(User.id == uuid_val)
                user = db.exec(stmt).first()
                logger.info(f"Found user in DB with UUID conversion: {user is not None}")
            except Exception as e2:
                logger.error(f"UUID conversion also failed: {e2}")
                user = None

        if user is None:
            logger.warning(f"User not found in database: {user_id}")
            raise credentials_exception

        logger.info(f"Successfully retrieved user: {user.id}")
        return user
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        logger.error(f"Unexpected error in get_current_user: {e}")
        logger.error(traceback.format_exc())
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        raise credentials_exception

def validate_user_id_from_token_and_path(token_user_id: str, path_user_id: str):
    """Validate that the user_id from JWT matches the user_id in the API path."""
    logger.info(f"Validating token user_id: {token_user_id} against path user_id: {path_user_id}")
    if token_user_id != path_user_id:
        logger.warning(f"User ID mismatch: token={token_user_id}, path={path_user_id}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID in token does not match user ID in path"
        )
    return True