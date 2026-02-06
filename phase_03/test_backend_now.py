"""Simple test to verify backend chat endpoint is working."""

import requests
import json
import base64

print("Testing Backend Chat Endpoint")
print("=" * 60)

# Step 1: Register test user
print("\n1. Registering test user...")
response = requests.post(
    "http://localhost:8000/register",
    json={"email": "test_now@test.com", "password": "test"}
)

if response.status_code != 200:
    print(f"❌ Registration failed: {response.status_code}")
    exit(1)

token = response.json()['access_token']
payload = token.split('.')[1] + '=' * (4 - len(token.split('.')[1]) % 4)
user_id = json.loads(base64.b64decode(payload)).get('sub')

print(f"✅ User ID: {user_id}")

# Step 2: Test with "eating" (no task command)
print("\n2. Testing with 'eating' (no task command)...")
response = requests.post(
    f"http://localhost:8000/api/{user_id}/chat",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    json={
        "message": "eating",
        "conversation_id": None
    }
)

print(f"Status: {response.status_code}")
print(f"Response:")
print(json.dumps(response.json(), indent=2))

# Step 3: Test with task command
print("\n3. Testing with 'Add task: Test task'...")
response = requests.post(
    f"http://localhost:8000/api/{user_id}/chat",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    json={
        "message": "Add task: Test task",
        "conversation_id": None
    }
)

print(f"Status: {response.status_code}")
print(f"Response:")
print(json.dumps(response.json(), indent=2))

# Step 4: Check tasks
print("\n4. Checking tasks...")
response = requests.get(
    f"http://localhost:8000/api/{user_id}/tasks",
    headers={"Authorization": f"Bearer {token}"}
)

tasks = response.json()
print(f"Tasks: {len(tasks)}")
for task in tasks:
    print(f"  - {task['title']}")

print("\n" + "=" * 60)
if len(tasks) > 0:
    print("✅ BACKEND IS WORKING!")
else:
    print("❌ BACKEND NOT CREATING TASKS")
