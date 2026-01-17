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
        self.SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "fallback_dev_secret_for_testing_only")
        if self.SECRET_KEY == "fallback_dev_secret_for_testing_only":
            print("WARNING: Using fallback secret key. Set BETTER_AUTH_SECRET environment variable for production.")
        
        self.ALGORITHM = "HS256"
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
            
            # Extract required fields - Better Auth may use different field names
            user_id: str = payload.get("userId") or payload.get("user_id") or payload.get("sub")
            email: str = payload.get("email") or payload.get("user_email")
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
            
            # Return user info
            return {
                "user_id": user_id,
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