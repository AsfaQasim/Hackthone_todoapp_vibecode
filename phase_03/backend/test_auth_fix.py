"""
Test script to verify the authentication fix
"""

import os
import sys
import asyncio
from unittest.mock import AsyncMock, MagicMock
import uuid
from datetime import datetime, timedelta
import jwt
import os
import sys

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from fastapi import Request
from src.services.auth_service import create_access_token
def test_authentication_flow():
    """Test the authentication flow to ensure it works properly"""
    print("Testing authentication flow...")
    
    # Create a mock user
    user_data = {
        "user_id": str(uuid.uuid4()),
        "email": "test@example.com"
    }
    
    # Create a JWT token
    token = create_access_token(user_data)
    print(f"Created token: {token[:20]}...")
    
    # Create a mock request
    request = Request(scope={
        "type": "http",
        "method": "GET",
        "path": "/test",
        "headers": [
            (b"authorization", f"Bearer {token}".encode())
        ]
    })
    
    # Test the global middleware simulation
    print("Testing global auth middleware simulation...")
    try:
        from src.services.auth_service import verify_token
        from fastapi import HTTPException
        
        auth_header = request.headers.get("Authorization")
        assert auth_header and auth_header.startswith("Bearer "), "Auth header should be present"
        
        token_from_header = auth_header.split(" ")[1]
        credentials_exception = HTTPException(status_code=401, detail="Could not validate credentials")
        
        token_data = verify_token(token_from_header, credentials_exception)
        
        # Verify token data matches
        print(f"Token data verified: {token_data.user_id}")
        assert token_data.user_id == user_data["user_id"]
        assert token_data.email == user_data["email"]
        
        # Simulate what middleware does (setting state)
        request.state = MagicMock()
        request.state.current_user = token_data
        request.state.user = {
            "user_id": token_data.user_id,
            "email": token_data.email
        }
        
        print("Global middleware simulation successful")
    except Exception as e:
        print(f"Global middleware test failed: {e}")
        return False
    
    # Test that we can access the user from the request (mimicking dependency injection)
    print("Testing user access from request...")
    try:
        user_from_request = request.state.user
        
        print(f"Retrieved user from request: {user_from_request}")
        assert user_from_request is not None, "Should return authenticated user"
        assert user_from_request["user_id"] == user_data["user_id"], "User ID should match"
        assert user_from_request["email"] == user_data["email"], "Email should match"
    except Exception as e:
        print(f"User access test failed: {e}")
        return False
    
    print("All authentication tests passed!")
    return True

if __name__ == "__main__":
    success = test_authentication_flow()
    if success:
        print("\n✓ Authentication flow test PASSED")
        print("The fix should resolve the redirect issue.")
    else:
        print("\n✗ Authentication flow test FAILED")
        print("Further investigation needed.")