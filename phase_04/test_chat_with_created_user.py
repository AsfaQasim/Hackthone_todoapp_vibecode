import jwt
import os
import requests
import json
from datetime import datetime, timedelta
import uuid

# Get the secret key from environment or use default
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-in-production")

# Use the user ID we created
user_id = "209c7989-187e-464d-935c-9ef245a3be95"  # The UUID from our created user
print(f"Using user ID: {user_id}")

# Create a valid token with proper structure
payload = {
    "sub": user_id,  # user ID in 'sub' field
    "email": "test_f570cb6a-c78d-42e0-8e6c-1f97cb60d185@example.com",  # email from our created user
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
    response = requests.post(f'http://localhost:8000/api/{user_id}/chat', headers=headers, json=data)
    print("\nChat endpoint response:", response.status_code)
    
    if response.status_code == 200:
        print("Response JSON:", response.json())
    else:
        print("Response text:", response.text)
        
except Exception as e:
    print("Chat endpoint request failed:", str(e))