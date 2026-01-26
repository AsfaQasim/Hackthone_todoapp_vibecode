"""
Simple test to verify the authentication components work together
"""

import os
import sys
import uuid
from datetime import datetime, timedelta
import jwt

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.services.auth_service import create_access_token
from middleware.auth_middleware import verify_user_is_authenticated
from fastapi import Request
from fastapi import HTTPException

def test_components():
    """Test that the authentication components work together"""
    print("Testing authentication components...")
    
    # Create a mock user
    user_data = {
        "user_id": str(uuid.uuid4()),
        "email": "test@example.com"
    }
    
    # Create a JWT token
    token = create_access_token(user_data)
    print(f"Created token for user: {user_data['user_id'][:8]}...")
    
    # Create a mock request with state
    class MockState:
        def __init__(self):
            self.user = user_data  # Set the user directly as the global middleware would
            self.current_user = None  # This would be set by the new middleware too
    
    request = Request(scope={
        "type": "http",
        "method": "GET",
        "path": "/test",
        "headers": [
            (b"authorization", f"Bearer {token}".encode())
        ]
    })
    request.state = MockState()
    
    # Test verify_user_is_authenticated
    print("Testing verify_user_is_authenticated with pre-authenticated user...")
    try:
        authenticated_user = verify_user_is_authenticated(request)
        print(f"Success! Returned user: {authenticated_user}")
        assert authenticated_user is not None, "Should return authenticated user"
        assert authenticated_user["user_id"] == user_data["user_id"], "User ID should match"
        assert authenticated_user["email"] == user_data["email"], "Email should match"
        print("✓ verify_user_is_authenticated works with pre-authenticated user")
    except Exception as e:
        print(f"✗ verify_user_is_authenticated failed: {e}")
        return False
    
    # Test with no authenticated user (should fail)
    print("\nTesting verify_user_is_authenticated with no authenticated user...")
    empty_request = Request(scope={
        "type": "http",
        "method": "GET",
        "path": "/test",
        "headers": []
    })
    empty_request.state = MockState()
    empty_request.state.user = None  # No authenticated user
    
    try:
        authenticated_user = verify_user_is_authenticated(empty_request)
        print("✗ Should have raised HTTPException but didn't")
        return False
    except HTTPException as e:
        print(f"✓ Correctly raised HTTPException: {e.detail}")
    except Exception as e:
        print(f"✗ Raised unexpected exception: {e}")
        return False
    
    print("\n✓ All component tests passed!")
    return True

if __name__ == "__main__":
    success = test_components()
    if success:
        print("\n✓ Authentication components integration test PASSED")
        print("The fix should resolve the redirect issue by ensuring:")
        print("- Global middleware authenticates requests")
        print("- Route-level authentication recognizes pre-authenticated users")
        print("- No redundant authentication attempts cause failures")
    else:
        print("\n✗ Authentication components integration test FAILED")
        print("Further investigation needed.")