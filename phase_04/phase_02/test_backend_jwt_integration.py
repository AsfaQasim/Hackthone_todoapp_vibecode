#!/usr/bin/env python3
"""
Test script to verify JWT integration between frontend and backend
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

import jwt
from datetime import datetime, timedelta
from backend.utils.jwt_handler import JWTHandler

def test_jwt_creation_and_verification():
    """Test that JWTs can be created and verified correctly"""
    print("Testing JWT creation and verification...")
    
    # Set the secret key for testing
    os.environ["BETTER_AUTH_SECRET"] = "dev_secret_for_testing_only"
    
    # Create a JWT handler instance
    jwt_handler = JWTHandler()
    
    # Create a test payload
    test_payload = {
        "sub": "test-user-id",  # Standard JWT claim for user ID
        "email": "test@example.com",
        "name": "Test User"
    }
    
    # Create a token
    token = jwt_handler.create_access_token(test_payload)
    print(f"Created token: {token[:50]}...")  # Print first 50 chars
    
    # Verify the token
    try:
        verified_payload = jwt_handler.verify_token(token)
        print(f"Verified payload: {verified_payload}")
        
        if verified_payload and verified_payload["user_id"] == "test-user-id":
            print("[PASS] JWT creation and verification test PASSED")
            return True
        else:
            print("[FAIL] JWT verification failed - incorrect payload")
            return False

    except Exception as e:
        print(f"[FAIL] JWT verification failed with error: {e}")
        return False

def test_cross_service_compatibility():
    """Test that tokens created with one method can be verified by the other"""
    print("\nTesting cross-service compatibility...")
    
    # Set the secret key for testing
    os.environ["BETTER_AUTH_SECRET"] = "dev_secret_for_testing_only"
    
    # Create a token using raw PyJWT (simulating frontend)
    SECRET_KEY = "dev_secret_for_testing_only"
    ALGORITHM = "HS256"
    
    frontend_payload = {
        "sub": "cross-test-user",
        "email": "cross-test@example.com",
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    
    frontend_token = jwt.encode(frontend_payload, SECRET_KEY, algorithm=ALGORITHM)
    print(f"Frontend-created token: {frontend_token[:50]}...")
    
    # Try to verify with backend JWT handler
    jwt_handler = JWTHandler()
    try:
        backend_verified = jwt_handler.verify_token(frontend_token)
        print(f"Backend verification result: {backend_verified}")
        
        if backend_verified and backend_verified["user_id"] == "cross-test-user":
            print("[PASS] Cross-service compatibility test PASSED")
            return True
        else:
            print("[FAIL] Cross-service compatibility failed")
            return False
    except Exception as e:
        print(f"[FAIL] Cross-service compatibility failed with error: {e}")
        return False

def test_sub_claim_priority():
    """Test that the 'sub' claim is prioritized for user_id"""
    print("\nTesting 'sub' claim priority...")
    
    os.environ["BETTER_AUTH_SECRET"] = "dev_secret_for_testing_only"
    
    # Create a token with multiple user ID fields
    SECRET_KEY = "dev_secret_for_testing_only"
    ALGORITHM = "HS256"
    
    payload_with_multiple_ids = {
        "sub": "primary-user-id",      # Should be prioritized
        "userId": "secondary-user-id", # Should be ignored
        "user_id": "tertiary-user-id", # Should be ignored
        "email": "multi-id-test@example.com",
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    
    token = jwt.encode(payload_with_multiple_ids, SECRET_KEY, algorithm=ALGORITHM)
    
    # Verify with backend JWT handler
    jwt_handler = JWTHandler()
    try:
        result = jwt_handler.verify_token(token)
        print(f"Result: {result}")
        
        if result and result["user_id"] == "primary-user-id":
            print("[PASS] 'sub' claim priority test PASSED")
            return True
        else:
            print(f"[FAIL] 'sub' claim priority failed. Expected 'primary-user-id', got '{result.get('user_id') if result else 'None'}'")
            return False
    except Exception as e:
        print(f"[FAIL] 'sub' claim priority test failed with error: {e}")
        return False

if __name__ == "__main__":
    print("Running JWT integration tests...\n")
    
    test_results = []
    test_results.append(test_jwt_creation_and_verification())
    test_results.append(test_cross_service_compatibility())
    test_results.append(test_sub_claim_priority())
    
    print(f"\n{'='*50}")
    print(f"Test Results: {sum(test_results)}/{len(test_results)} tests passed")

    if all(test_results):
        print("[SUCCESS] All JWT integration tests PASSED!")
        exit(0)
    else:
        print("[FAILURE] Some JWT integration tests FAILED!")
        exit(1)