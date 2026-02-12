"""
Test script to verify the frontend API routes work correctly with auth_token cookies
"""
import requests
import json

def test_frontend_login():
    print("Testing frontend login API route...")
    
    # Prepare login data
    login_data = {
        "email": "test@example.com",
        "password": "password123"
    }
    
    # Send login request to frontend which should forward to backend
    response = requests.post('http://localhost:3000/api/login', json=login_data)
    
    print(f"Frontend login response status: {response.status_code}")
    print(f"Frontend login response: {response.text}")
    
    # Check if auth_token cookie is set
    cookies = response.cookies
    auth_token = cookies.get('auth_token')
    print(f"Auth token cookie set: {auth_token is not None}")
    
    if auth_token:
        print(f"Auth token value: {auth_token[:20]}...")  # Show first 20 chars
    
    return response, cookies

def test_frontend_verify_token(cookies):
    print("\nTesting frontend verify-token API route...")
    
    # Send verify-token request with cookies
    response = requests.get('http://localhost:3000/api/verify-token', cookies=cookies)
    
    print(f"Frontend verify-token response status: {response.status_code}")
    print(f"Frontend verify-token response: {response.text}")
    
    return response

if __name__ == "__main__":
    # First test the frontend login
    response, cookies = test_frontend_login()
    
    # Then test the verify-token endpoint if login was successful
    if cookies.get('auth_token'):
        test_frontend_verify_token(cookies)
    else:
        print("Skipping verify-token test since no auth_token cookie was set")