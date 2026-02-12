import jwt
import os
from datetime import datetime, timedelta

# Get the secret key from environment or use default
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-in-production")
print(f"Using secret key: {SECRET_KEY}")

# Create a token
payload = {
    "sub": "8e9721fd-b201-42c4-a764-c0391b68d271",  # canonical format
    "email": "test@example.com",
    "exp": datetime.utcnow() + timedelta(hours=1)
}

token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
print(f"Encoded token: {token}")

# Try to decode it
try:
    decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    print(f"Decoded payload: {decoded_payload}")
    print("Token verification succeeded!")
except jwt.ExpiredSignatureError:
    print("Token has expired")
except jwt.InvalidTokenError as e:
    print(f"Invalid token: {e}")
except Exception as e:
    print(f"Other error: {e}")