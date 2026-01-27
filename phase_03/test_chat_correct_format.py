import jwt
import os
import requests
import json
from datetime import datetime, timedelta
import uuid

# Get the secret key from environment or use default
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-in-production")

# Use the actual user ID from the database (hex format without dashes)
# From our database check, we have several users. Let's use one of them:
user_id_hex = "8e9721fdb20142c4a764c0391b68d271"  # This is the hex representation without dashes
user_email = "test@example.com"

# Convert the hex string back to a proper UUID for the token
user_uuid = uuid.UUID(hex=user_id_hex)
user_id_canonical = str(user_uuid)  # This will be in canonical format with dashes

print(f"Hex user ID (stored in DB): {user_id_hex}")
print(f"Canonical user ID (for token): {user_id_canonical}")

# Create a valid token with proper structure using the canonical UUID
payload = {
    "sub": user_id_canonical,  # user ID in 'sub' field (canonical format with dashes)
    "email": user_email,
    "exp": datetime.utcnow() + timedelta(hours=1)
}

token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

print("Generated test token:", token)

# Test the chat endpoint with the valid token, using the canonical UUID in the path
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {token}'
}

data = {
    'message': 'Hello, can you help me create a task?',
    'conversation_id': None
}

try:
    # Use the canonical UUID format in the path
    response = requests.post(f'http://localhost:8000/api/{user_id_canonical}/chat', headers=headers, json=data)
    print("\nChat endpoint response:", response.status_code)
    
    if response.status_code == 200:
        print("Response JSON:", response.json())
    else:
        print("Response text:", response.text)
        
except Exception as e:
    print("Chat endpoint request failed:", str(e))