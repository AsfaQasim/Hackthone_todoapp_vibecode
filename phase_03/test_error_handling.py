"""Test script to verify backend error handling returns proper JSON responses."""

import requests
import json

def test_backend_error_handling():
    """Test that backend returns JSON responses even for errors."""
    base_url = "http://localhost:8000"
    
    print("Testing backend error handling...")
    
    # Test 1: Health check (should work)
    try:
        response = requests.get(f"{base_url}/health")
        print(f"Health check - Status: {response.status_code}")
        try:
            data = response.json()
            print(f"Health check - JSON response: {data}")
        except:
            print(f"Health check - Non-JSON response: {response.text}")
    except Exception as e:
        print(f"Health check failed: {e}")
    
    # Test 2: Invalid endpoint (should return JSON error)
    try:
        response = requests.get(f"{base_url}/invalid-endpoint")
        print(f"\nInvalid endpoint - Status: {response.status_code}")
        try:
            data = response.json()
            print(f"Invalid endpoint - JSON response: {data}")
        except:
            print(f"Invalid endpoint - Non-JSON response: {response.text}")
    except Exception as e:
        print(f"Invalid endpoint test failed: {e}")
    
    # Test 3: Try to trigger an error in the chat endpoint
    try:
        # This should fail due to missing user_id in path, but should return JSON
        response = requests.post(f"{base_url}/api/chat", json={"message": "test"})
        print(f"\nInvalid chat endpoint - Status: {response.status_code}")
        try:
            data = response.json()
            print(f"Invalid chat endpoint - JSON response: {data}")
        except:
            print(f"Invalid chat endpoint - Non-JSON response: {response.text}")
    except Exception as e:
        print(f"Invalid chat endpoint test failed: {e}")

if __name__ == "__main__":
    test_backend_error_handling()