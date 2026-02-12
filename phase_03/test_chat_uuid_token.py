import jwt
import os
import requests
import json
from datetime import datetime, timedelta
import uuid

# Create a mock token for testing
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-in-production")

# Create a valid token with proper UUID structure
user_id = str(uuid.uuid4())  # Generate a proper UUID
payload = {
    "sub": user_id,  # user ID as UUID
    "email": "test@example.com",
    "exp": datetime.utcnow() + timedelta(hours=1)
}

token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

print("Generated test token:", token)
print("User ID (UUID):", user_id)

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
    response = requests.post(f'http://localhost:8000/api/{user_id}/chat', headers=headers, json=data)
    print("\nChat endpoint response:", response.status_code)
    print("Response JSON:", response.json())
except Exception as e:
    print("Chat endpoint request failed:", str(e))