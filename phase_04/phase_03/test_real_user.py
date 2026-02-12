"""Test with the real user asfaqasim145@gmail.com"""

import requests
import json

# Your email
USER_EMAIL = "asfaqasim145@gmail.com"

print("Testing with real user:", USER_EMAIL)
print("=" * 60)

# First, let's try to login (if this user exists in backend)
print("\n1. Trying to login...")
response = requests.post(
    "http://localhost:8000/login",
    json={"email": USER_EMAIL, "password": "password123"}
)

if response.status_code == 200:
    data = response.json()
    token = data.get('access_token')
    print(f"✅ Login successful!")
    print(f"   Token: {token[:30]}...")
    
    # Decode token to get user ID
    import base64
    payload = token.split('.')[1]
    payload += '=' * (4 - len(payload) % 4)
    decoded = json.loads(base64.b64decode(payload))
    user_id = decoded.get('sub') or decoded.get('userId') or decoded.get('user_id')
    print(f"   User ID: {user_id}")
    
    # Test chat endpoint
    print(f"\n2. Testing chat endpoint...")
    print(f"   Sending: 'Add task: Test from real user'")
    
    response = requests.post(
        f"http://localhost:8000/api/{user_id}/chat",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json={
            "message": "Add task: Test from real user",
            "conversation_id": None
        }
    )
    
    print(f"\n   Status: {response.status_code}")
    print(f"   Response:")
    print(json.dumps(response.json(), indent=2))
    
    # Check tasks
    print(f"\n3. Checking tasks...")
    response = requests.get(
        f"http://localhost:8000/api/{user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        tasks = response.json()
        print(f"✅ Tasks found: {len(tasks)}")
        for task in tasks:
            print(f"   - {task.get('title')} ({task.get('status')})")
    else:
        print(f"❌ Failed to get tasks: {response.status_code}")
        print(response.text)
        
else:
    print(f"❌ Login failed: {response.status_code}")
    print(f"   Response: {response.text}")
    print(f"\n   This user might not exist in backend database.")
    print(f"   The frontend uses Better Auth which stores users differently.")
