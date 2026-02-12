import jwt
import os
import requests
import json
from datetime import datetime, timedelta
import uuid

# Get the secret key from environment or use default
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-in-production")

# Use the actual user ID from the backend database
user_id_canonical = "8e9721fd-b201-42c4-a764-c0391b68d271"  # Canonical format with dashes
user_id_hex = uuid.UUID(user_id_canonical).hex  # Convert to hex format without dashes
user_email = "test@example.com"

print(f"Canonical user ID (with dashes): {user_id_canonical}")
print(f"Hex user ID (no dashes): {user_id_hex}")
print(f"User email: {user_email}")

# Create a valid token with the canonical format (this is what clients typically send)
payload = {
    "sub": user_id_canonical,  # Use canonical format in token
    "email": user_email,
    "exp": datetime.utcnow() + timedelta(hours=1)
}

token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

print("Generated test token:", token)

# Test the chat endpoint with the valid token using canonical format in path
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'
}

data = {
    'message': 'Hello, can you help me create a task?',
    'conversation_id': None
}

try:
    # Test with canonical format in the path
    response = requests.post(f'http://localhost:8000/api/{user_id_canonical}/chat', headers=headers, json=data)
    print(f"\nChat endpoint response (canonical format): {response.status_code}")
    
    if response.status_code == 200:
        print("Response JSON:", response.json())
    else:
        print("Response text:", response.text)
        
    # Also try with hex format in the path
    response_hex = requests.post(f'http://localhost:8000/api/{user_id_hex}/chat', headers=headers, json=data)
    print(f"\nChat endpoint response (hex format): {response_hex.status_code}")
    
    if response_hex.status_code == 200:
        print("Response JSON:", response_hex.json())
    else:
        print("Response text:", response_hex.text)
        
except Exception as e:
    print("Chat endpoint request failed:", str(e))