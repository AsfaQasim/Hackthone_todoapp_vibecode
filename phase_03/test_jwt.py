import jwt
from datetime import datetime, timedelta
import os

# JWT configuration - using BETTER_AUTH_SECRET for Better Auth compatibility
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "fallback_dev_secret_for_testing_only")
ALGORITHM = "HS256"

def create_test_token():
    """Create a test token"""
    from datetime import datetime, timedelta
    data = {"user_id": "test-user-id", "email": "test@example.com"}

    # Create a token that expires in 24 hours to avoid expiration issues during testing
    expire = datetime.utcnow() + timedelta(hours=24)  # 24 hour expiry for testing
    data.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_test_token(token: str):
    """Verify the test token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded payload: {payload}")

        user_id: str = payload.get("user_id")
        email: str = payload.get("email")
        exp: int = payload.get("exp")

        print(f"user_id: {user_id}")
        print(f"email: {email}")
        print(f"exp: {exp}")

        if user_id is None or email is None or exp is None:
            print("Missing required fields in token")
            return None

        # Check if token is expired - using datetime objects for accurate comparison
        current_time = datetime.utcnow()
        exp_datetime = datetime.fromtimestamp(exp)

        if current_time > exp_datetime:
            print("Token is expired")
            return None

        print("Token is valid!")
        return {"user_id": user_id, "email": email, "exp": exp}
    except jwt.ExpiredSignatureError:
        print("Token has expired")
        return None
    except jwt.InvalidTokenError as e:
        print(f"Invalid token: {e}")
        return None

# Test token creation and verification
token = create_test_token()
print(f"Generated token: {token}")
result = verify_test_token(token)
print(f"Verification result: {result}")