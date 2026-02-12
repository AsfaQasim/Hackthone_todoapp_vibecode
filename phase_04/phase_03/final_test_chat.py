import jwt
import os
import requests
import json
from datetime import datetime, timedelta

# Use one of the user IDs from the database
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-in-production")

# Use the user ID we know exists in the database: 776e40cf-6874-43a2-bb12-b43f117df73c
user_id = "776e40cf-6874-43a2-bb12-b43f117df73c"
payload = {
    "sub": user_id,  # user ID that exists in the database
    "email": "test_d327a7f6-0a8b-493e-ac3c-80ff4260685a@example.com",  # email from the database
    "exp": datetime.utcnow() + timedelta(hours=1)
}

token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

print("Generated test token for verification:", token[:50] + "...")
print("User ID (from database):", user_id)

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
        print("✅ SUCCESS: Chat endpoint responded with 200 OK")
        print("Response JSON:", json.dumps(response.json(), indent=2))
    elif response.status_code == 401:
        print("❌ FAILED: Authentication still failing")
        print("Response text:", response.text)
    else:
        print(f"⚠️  OTHER STATUS: Chat endpoint responded with {response.status_code}")
        print("Response text:", response.text[:500])
except Exception as e:
    print("❌ REQUEST FAILED:", str(e))
    import traceback
    traceback.print_exc()