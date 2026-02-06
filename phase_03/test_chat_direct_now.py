"""Test chat endpoint directly to see what's happening."""

import requests
import json

# First, register a test user
print("1. Registering test user...")
response = requests.post(
    "http://localhost:8000/register",
    json={"email": "test_direct@example.com", "password": "test123"}
)

if response.status_code == 200:
    data = response.json()
    token = data['access_token']
    
    # Decode token to get user ID
    import base64
    payload = token.split('.')[1]
    payload += '=' * (4 - len(payload) % 4)
    decoded = json.loads(base64.b64decode(payload))
    user_id = decoded.get('sub') or decoded.get('userId')
    
    print(f"✅ User registered: {user_id}")
    print(f"   Token: {token[:30]}...")
    
    # Test chat endpoint
    print(f"\n2. Testing chat endpoint...")
    print(f"   Sending: 'Add a task: Test task creation'")
    
    response = requests.post(
        f"http://localhost:8000/api/{user_id}/chat",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json={
            "message": "Add a task: Test task creation",
            "conversation_id": None
        }
    )
    
    print(f"\n   Status: {response.status_code}")
    print(f"   Response:")
    print(json.dumps(response.json(), indent=2))
    
else:
    print(f"❌ Registration failed: {response.status_code}")
    print(response.text)
