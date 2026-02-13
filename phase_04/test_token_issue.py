"""Test token verification issue."""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from src.services.auth_service import verify_token, create_access_token
from src.config import settings

print("Testing token verification...")
print("=" * 70)

# Test 1: Create a token
print("\n1. Creating a test token...")
test_payload = {
    "sub": "test-user-id",
    "email": "asfaqasim145@gmail.com",
    "name": "Test User"
}

token = create_access_token(test_payload)
print(f"   Token created: {token[:50]}...")
print(f"   JWT Secret: {settings.jwt_secret[:20]}...")

# Test 2: Verify the token
print("\n2. Verifying the token...")
try:
    payload = verify_token(token)
    print(f"   ✅ Token verified successfully!")
    print(f"   Payload: {payload}")
except Exception as e:
    print(f"   ❌ Token verification failed: {e}")

# Test 3: Check what secret is being used
print("\n3. Checking JWT configuration...")
print(f"   BETTER_AUTH_SECRET from env: {os.getenv('BETTER_AUTH_SECRET', 'NOT SET')[:20]}...")
print(f"   JWT_SECRET from env: {os.getenv('JWT_SECRET', 'NOT SET')[:20]}...")
print(f"   Settings secret_key: {settings.secret_key[:20]}...")
print(f"   Settings jwt_secret: {settings.jwt_secret[:20]}...")

print("\n" + "=" * 70)
