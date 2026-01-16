#!/usr/bin/env python
"""
Test script to verify the Better Auth JWT token handling in the backend
"""
import asyncio
import os
import sys
# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from datetime import timedelta
from utils.jwt_handler import create_access_token, verify_better_auth_token, get_token_from_request
from fastapi import Request
from unittest.mock import Mock

# Test token creation and verification
def test_token_creation_verification():
    print("Testing token creation and verification...")
    
    # Test data
    test_data = {
        "user_id": "test-user-123",
        "email": "test@example.com"
    }
    
    # Create a token
    token = create_access_token(data=test_data, expires_delta=timedelta(hours=1))  # 1 hour expiry to avoid timing issues
    print(f"Created token: {token[:50]}...")  # Show first 50 chars
    
    # Verify the token
    token_data = verify_better_auth_token(token)
    
    if token_data:
        print(f"[PASS] Token verified successfully")
        print(f"  User ID: {token_data.user_id}")
        print(f"  Email: {token_data.email}")
        assert token_data.user_id == test_data["user_id"]
        assert token_data.email == test_data["email"]
        print("[PASS] Token data matches expected values")
    else:
        print("[FAIL] Failed to verify token")
        return False
        
    return True

# Test token extraction from request
def test_token_extraction():
    print("\nTesting token extraction from request...")
    
    # Create a mock request with Authorization header
    mock_request = Mock(spec=Request)
    mock_request.headers = {"Authorization": "Bearer test-token-123"}
    mock_request.cookies = {}
    mock_request.state = Mock()
    mock_request.state.better_auth_token = None
    
    try:
        extracted_token = get_token_from_request(mock_request)
        print(f"[PASS] Extracted token from header: {extracted_token}")
        assert extracted_token == "test-token-123"
    except Exception as e:
        print(f"[FAIL] Error extracting token from header: {e}")
        return False

    # Test with cookie
    mock_request = Mock(spec=Request)
    mock_request.headers = {}  # No authorization header
    mock_request.cookies = {"better-auth.session_token": "cookie-token-456"}
    mock_request.state = Mock()
    mock_request.state.better_auth_token = None

    try:
        extracted_token = get_token_from_request(mock_request)
        print(f"[PASS] Extracted token from cookie: {extracted_token}")
        assert extracted_token == "cookie-token-456"
    except Exception as e:
        print(f"[FAIL] Error extracting token from cookie: {e}")
        return False

    # Test with request state (middleware)
    mock_request = Mock(spec=Request)
    mock_request.headers = {}  # No authorization header
    mock_request.cookies = {}  # No cookies
    mock_request.state = Mock()
    mock_request.state.better_auth_token = "state-token-789"

    try:
        extracted_token = get_token_from_request(mock_request)
        print(f"[PASS] Extracted token from request state: {extracted_token}")
        assert extracted_token == "state-token-789"
    except Exception as e:
        print(f"[FAIL] Error extracting token from request state: {e}")
        return False
    
    return True

async def main():
    print("Starting Better Auth JWT implementation tests...\n")
    
    # Set environment variable for testing
    os.environ["BETTER_AUTH_SECRET"] = "test-secret-key-for-testing-purposes-only"
    
    success = True
    
    # Test token creation and verification
    success &= test_token_creation_verification()
    
    # Test token extraction
    success &= test_token_extraction()
    
    if success:
        print("\n[PASS] All tests passed! Better Auth JWT implementation is working correctly.")
    else:
        print("\n[FAIL] Some tests failed!")

    return success

if __name__ == "__main__":
    asyncio.run(main())