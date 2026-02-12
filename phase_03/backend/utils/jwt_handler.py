import jwt
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from fastapi import HTTPException, status


class JWTHandler:
    """
    JWT Handler class for creating and verifying JWT tokens
    following the Better Auth integration specification.
    """

    def __init__(self):
        # Use the same secret key as Better Auth for compatibility
        # Use the same secret as the auth service for consistency
        self.SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-in-production")
        if not self.SECRET_KEY:
            raise RuntimeError(
                "BETTER_AUTH_SECRET environment variable is not set.\n"
                "Please set BETTER_AUTH_SECRET for production use.\n"
                "For development, add 'BETTER_AUTH_SECRET=dev_secret_for_testing_only' to your environment."
            )

        self.ALGORITHM = "HS256"  # Strictly enforce HS256 algorithm
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days expiry as per spec

    def create_access_token(self, data: dict) -> str:
        """
        Create a JWT access token with the provided data
        """
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Verify a JWT token and return the payload if valid
        """
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])

            # Extract required fields - Support multiple possible field names for compatibility
            # Try multiple possible field names for user_id
            user_id: str = payload.get("sub") or payload.get("userId") or payload.get("user_id")
            # Try multiple possible field names for email
            email: str = payload.get("email") or payload.get("user_email") or payload.get("sub_email")
            exp_timestamp: int = payload.get("exp")

            # Validate required fields exist
            if not user_id or not email or exp_timestamp is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token missing required fields"
                )

            # Check if token is expired
            current_time = datetime.utcnow().timestamp()
            if current_time > exp_timestamp:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired"
                )

            # Return user info with standardized field names
            return {
                "user_id": user_id,  # Map 'sub' from Better Auth to 'user_id' for internal use
                "email": email,
                "exp": exp_timestamp
            }
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token verification error: {str(e)}"
            )


# Global instance
jwt_handler = JWTHandler()


def get_current_user(token: str) -> Dict[str, Any]:
    """
    Dependency function to get current user from token
    """
    return jwt_handler.verify_token(token)