"""Test smart AI task creation"""
import requests
import json
import base64
import time

BASE_URL = "http://localhost:8000"

print("=" * 70)
print("SMART AI TASK CREATION TEST")
print("=" * 70)

# Register user
email = f"test_{int(time.time())}@test.com"
response = requests.post(f"{BASE_URL}/register", json={"email": email, "password": "test"})
token = response.json()['access_token']
payload = token.split('.')[1] + '=' * (4 - len(token.split('.')[1]) % 4)
user_id = json.loads(base64.b64decode(payload)).get('sub')

print(f"\n✅ User: {email} (ID: {user_id})")

# Test cases
test_messages = [
    "eating",
    "playing",
    "shopping for groceries",
    "call mom",
    "finish homework"
]

print("\n" + "=" * 70)
print("TESTING SMART TASK CREATION")
print("=" * 70)

for msg in test_messages:
    print(f"\n📨 Message: '{msg}'")
    response = requests.post(
        f"{BASE_URL}/api/{user_id}/chat",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"message": msg}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"   Response: {data.get('response', '')[:80]}...")
        if data.get('tool_calls'):
            print(f"   ✅ Task created: {data['tool_calls'][0]['arguments']['title']}")
        else:
            print(f"   ℹ️  No task created (general response)")
    else:
        print(f"   ❌ Error: {response.status_code}")

# List all tasks
print("\n" + "=" * 70)
print("FINAL TASK LIST")
print("=" * 70)

response = requests.post(
    f"{BASE_URL}/api/{user_id}/chat",
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    json={"message": "list tasks"}
)

if response.status_code == 200:
    data = response.json()
    print(data.get('response', ''))
else:
    print(f"❌ Error: {response.status_code}")

print("\n" + "=" * 70)
