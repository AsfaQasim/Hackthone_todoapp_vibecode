"""Test local chat endpoint"""
import requests
import json

# Test user credentials
TEST_USER = {
    "email": "asfaqasim145@gmail.com",
    "password": "test123"  # Replace with your actual password
}

BACKEND_URL = "http://localhost:8000"

print("=" * 80)
print("🧪 TESTING LOCAL CHAT ENDPOINT")
print("=" * 80)

# Step 1: Login to get token
print("\n1️⃣ Logging in...")
try:
    response = requests.post(
        f"{BACKEND_URL}/login",
        json=TEST_USER,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        token = data.get("token")
        user_id = data.get("user_id")
        print(f"   ✅ Login successful!")
        print(f"   User ID: {user_id}")
        print(f"   Token: {token[:30]}...")
    else:
        print(f"   ❌ Login failed: {response.status_code}")
        print(f"   Response: {response.text}")
        exit(1)
except Exception as e:
    print(f"   ❌ Login error: {e}")
    exit(1)

# Step 2: Test chat with simple message
print("\n2️⃣ Testing chat with 'playing games'...")
try:
    response = requests.post(
        f"{BACKEND_URL}/api/{user_id}/chat",
        json={"message": "playing games"},
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )
    
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Chat response:")
        print(f"   Response: {data.get('response')}")
        print(f"   Tool calls: {len(data.get('tool_calls', []))}")
        if data.get('tool_calls'):
            for tool in data['tool_calls']:
                print(f"      - {tool.get('tool_name')}: {tool.get('result', {}).get('message')}")
    else:
        print(f"   ❌ Chat failed: {response.status_code}")
        print(f"   Response: {response.text}")
        
except Exception as e:
    print(f"   ❌ Chat error: {e}")
    import traceback
    traceback.print_exc()

# Step 3: Check if task was created
print("\n3️⃣ Checking tasks...")
try:
    response = requests.get(
        f"{BACKEND_URL}/api/{user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        tasks = response.json()
        print(f"   ✅ Found {len(tasks)} tasks")
        for task in tasks[-3:]:  # Show last 3 tasks
            print(f"      - {task.get('title')} ({task.get('status')})")
    else:
        print(f"   ❌ Get tasks failed: {response.status_code}")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"   ❌ Get tasks error: {e}")

print("\n" + "=" * 80)
print("✅ TEST COMPLETE")
print("=" * 80)
