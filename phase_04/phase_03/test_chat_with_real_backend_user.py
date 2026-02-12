import jwt
import os
import requests
import json
from datetime import datetime, timedelta

# Get the secret key from environment or use default
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-in-production")

# Use the actual user ID from the backend database
user_id = "8e9721fd-b201-42c4-a764-c0391b68d271"  # This is the hex representation from the DB
user_email = "test@example.com"

print(f"Using user ID from backend DB: {user_id}")
print(f"User email: {user_email}")

# Create a valid token with proper structure
payload = {
    "sub": user_id,  # Use the exact user ID from the database
    "email": user_email,
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
    # Use the exact user ID from the database in the path
    response = requests.post(f'http://localhost:8000/api/{user_id}/chat', headers=headers, json=data)
    print("\nChat endpoint response:", response.status_code)
    
    if response.status_code == 200:
        print("Response JSON:", response.json())
    else:
        print("Response text:", response.text)
        
except Exception as e:
    print("Chat endpoint request failed:", str(e))