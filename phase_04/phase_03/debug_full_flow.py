"""Complete debugging script to test the full flow."""

import requests
import json
import time

print("=" * 70)
print("COMPLETE FLOW DEBUGGING")
print("=" * 70)

# Step 1: Check backend health
print("\n1. Checking backend health...")
try:
    response = requests.get("http://localhost:8000/health", timeout=5)
    if response.status_code == 200:
        print("✅ Backend is running")
    else:
        print(f"❌ Backend returned {response.status_code}")
        exit(1)
except Exception as e:
    print(f"❌ Backend not accessible: {e}")
    exit(1)

# Step 2: Register a test user
print("\n2. Registering test user...")
test_email = f"debug_user_{int(time.time())}@test.com"
response = requests.post(
    "http://localhost:8000/register",
    json={"email": test_email, "password": "test123"}
)

if response.status_code != 200:
    print(f"❌ Registration failed: {response.status_code}")
    print(response.text)
    exit(1)

data = response.json()
token = data['access_token']
print(f"✅ User registered: {test_email}")
print(f"   Token: {token[:30]}...")

# Decode token to get user ID
import base64
payload = token.split('.')[1]
payload += '=' * (4 - len(payload) % 4)
decoded = json.loads(base64.b64decode(payload))
user_id = decoded.get('sub') or decoded.get('userId') or decoded.get('user_id')
print(f"   User ID: {user_id}")

# Step 3: Test chat endpoint with task creation
print("\n3. Testing chat endpoint...")
print("   Sending: 'Add task: Debug test task'")

response = requests.post(
    f"http://localhost:8000/api/{user_id}/chat",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    json={
        "message": "Add task: Debug test task",
        "conversation_id": None
    }
)

print(f"\n   Status: {response.status_code}")

if response.status_code == 200:
    data = response.json()
    print(f"   ✅ Chat response received")
    print(f"   Response: {data.get('response', '')[:80]}...")
    
    tool_calls = data.get('tool_calls', [])
    if tool_calls:
        print(f"   Tool calls: {len(tool_calls)}")
        for call in tool_calls:
            print(f"      - {call.get('tool_name')}: {call.get('result', {}).get('success')}")
    else:
        print(f"   ⚠️ No tool calls (task might not have been created)")
else:
    print(f"   ❌ Chat failed: {response.status_code}")
    print(f"   Response: {response.text}")
    exit(1)

# Step 4: Verify task was created
print("\n4. Checking if task was created...")
response = requests.get(
    f"http://localhost:8000/api/{user_id}/tasks",
    headers={"Authorization": f"Bearer {token}"}
)

if response.status_code == 200:
    tasks = response.json()
    print(f"   ✅ Tasks retrieved: {len(tasks)} tasks")
    
    if tasks:
        print(f"\n   Tasks in database:")
        for task in tasks:
            print(f"      - {task.get('title')} ({task.get('status')})")
            print(f"        ID: {task.get('id')}")
            print(f"        User ID: {task.get('user_id')}")
    else:
        print(f"   ⚠️ No tasks found!")
        print(f"   This means task creation failed silently")
else:
    print(f"   ❌ Failed to get tasks: {response.status_code}")
    print(f"   Response: {response.text}")

# Step 5: Summary
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"User: {test_email}")
print(f"User ID: {user_id}")
print(f"Chat response: {'✅ Success' if response.status_code == 200 else '❌ Failed'}")
print(f"Tasks created: {len(tasks) if 'tasks' in locals() else 0}")

if len(tasks) > 0:
    print(f"\n✅ EVERYTHING WORKING!")
    print(f"   - User can be created")
    print(f"   - Chat endpoint responds")
    print(f"   - Tasks are created")
    print(f"   - Tasks can be retrieved")
    print(f"\n   The issue might be with frontend authentication.")
    print(f"   Your user (asfaqasim145@gmail.com) might have a different user ID format.")
else:
    print(f"\n❌ TASK CREATION FAILED")
    print(f"   - Chat endpoint responds but doesn't create tasks")
    print(f"   - Check backend logs for errors")

print("=" * 70)
