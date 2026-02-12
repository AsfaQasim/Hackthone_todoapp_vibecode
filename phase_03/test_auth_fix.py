"""
Test script to verify the authentication fix
"""
import requests
import json

# Test the backend login endpoint directly
def test_backend_login():
    print("Testing backend login endpoint...")
    
    # Prepare login data
    login_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    
    # Send login request to backend
    response = requests.post('http://localhost:8000/login', json=login_data)
    
    print(f"Backend login response status: {response.status_code}")
    print(f"Backend login response: {response.text}")
    
    if response.status_code == 200:
        response_data = response.json()
        print(f"Access token received: {'access_token' in response_data}")
        
        # Test the verify-token endpoint with the received token
        token = response_data.get('access_token')
        if token:
            headers = {
                'Authorization': f'Bearer {token}'
            }
            verify_response = requests.get('http://localhost:8000/verify-token', headers=headers)
            print(f"Backend verify-token response status: {verify_response.status_code}")
            print(f"Backend verify-token response: {verify_response.text}")
    
    return response

if __name__ == "__main__":
    test_backend_login()