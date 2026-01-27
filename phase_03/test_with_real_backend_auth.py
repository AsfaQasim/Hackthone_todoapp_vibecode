import requests
import json

# Try to login with a test user to get a valid token from the backend
login_data = {
    "email": "test@example.com",
    "password": "test123"  # Default test password
}

try:
    response = requests.post('http://localhost:8000/api/login', json=login_data)
    print(f"Login response: {response.status_code}")
    print(f"Login response text: {response.text}")
    
    if response.status_code == 200:
        login_response = response.json()
        token = login_response.get('token')
        print(f"Received token: {token}")
        
        # Now try to use this token with the chat endpoint
        if token:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {token}'
            }
            
            chat_data = {
                'message': 'Hello, can you help me create a task?',
                'conversation_id': None
            }
            
            # Use the user's actual ID from the database (canonical format)
            user_id = "8e9721fd-b201-42c4-a764-c0391b68d271"
            chat_response = requests.post(f'http://localhost:8000/api/{user_id}/chat', headers=headers, json=chat_data)
            print(f"\nChat endpoint response: {chat_response.status_code}")
            print(f"Chat response text: {chat_response.text}")
    else:
        print("Login failed - let's try to register the user first")
        
        # Try to register the user
        register_data = {
            "email": "test@example.com",
            "password": "test123",
            "name": "Test User"
        }
        
        reg_response = requests.post('http://localhost:8000/api/register', json=register_data)
        print(f"Registration response: {reg_response.status_code}")
        print(f"Registration response text: {reg_response.text}")
        
except Exception as e:
    print(f"Request failed: {str(e)}")