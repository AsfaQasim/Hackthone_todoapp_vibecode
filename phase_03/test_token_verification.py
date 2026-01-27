import jwt
import os
from datetime import datetime, timedelta

# Get the secret key from environment
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-in-production")
print(f"Using secret key: {SECRET_KEY}")

# Test token creation and verification
payload = {
    "sub": "8e9721fd-b201-42c4-a764-c0391b68d271",  # Known user ID from DB
    "email": "test@example.com",
    "exp": datetime.utcnow() + timedelta(hours=1)
}

# Create a token
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
print(f"Created token: {token}")

# Verify the token
try:
    decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    print(f"Successfully decoded token: {decoded}")
except Exception as e:
    print(f"Error decoding token: {e}")

# Also test with a fake token to see what happens
fake_token = "invalid.token.here"
try:
    decoded_fake = jwt.decode(fake_token, SECRET_KEY, algorithms=["HS256"])
    print(f"Fake token decoded: {decoded_fake}")
except Exception as e:
    print(f"Expected error with fake token: {e}")