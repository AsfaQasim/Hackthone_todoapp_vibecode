import requests
import json

# Test chat endpoint
print("Testing chat endpoint...")

# First login to get token
login_data = {
    "email": "asfaqasim145@gmail.com",
    "password": "test123"
}

print("\n1. Logging in...")
login_response = requests.post("http://localhost:8000/login", json=login_data)
print(f"Login status: {login_response.status_code}")

if login_response.status_code == 200:
    login_result = login_response.json()
    print(f"Login successful!")
    print(f"User ID: {login_result.get('user_id')}")
    
    # Get token from response
    token = login_result.get('access_token')
    user_id = login_result.get('user_id')
    
    if token and user_id:
        print(f"\n2. Testing chat endpoint...")
        
        # Test chat
        chat_data = {
            "message": "Hello, can you help me?",
            "conversation_id": None
        }
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        chat_url = f"http://localhost:8000/api/{user_id}/chat"
        print(f"Chat URL: {chat_url}")
        
        chat_response = requests.post(chat_url, json=chat_data, headers=headers)
        print(f"Chat status: {chat_response.status_code}")
        
        if chat_response.status_code == 200:
            chat_result = chat_response.json()
            print(f"✅ Chat successful!")
            print(f"Response: {chat_result.get('response', 'No response')[:100]}...")
        else:
            print(f"❌ Chat failed!")
            print(f"Error: {chat_response.text}")
    else:
        print("❌ No token or user_id in login response")
else:
    print(f"❌ Login failed: {login_response.text}")
