import jwt
import os
import requests
import json
from datetime import datetime, timedelta

# Create a mock token for testing
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-in-production")

# Create a valid token with proper structure
payload = {
    "sub": "test_user_123",  # user ID in 'sub' field
    "email": "test@example.com",
    "exp": datetime.utcnow() + timedelta(hours=1)
}

token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

print("Generated test token:", token)

# Test the chat endpoint with the valid token
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'
}

data = {
    'message': 'Hello, can you help me create a task?',
    'conversation_id': None
}

try:
    response = requests.post('http://localhost:8000/api/test_user_123/chat', headers=headers, json=data)
    print("\nChat endpoint response:", response.status_code)
    print("Response JSON:", response.json())
except Exception as e:
    print("Chat endpoint request failed:", str(e))