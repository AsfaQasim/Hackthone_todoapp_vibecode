"""Complete end-to-end test with user creation, chat, and task verification"""
import requests
import json
import base64
import time

BASE_URL = "http://localhost:8000"

print("=" * 70)
print("COMPLETE END-TO-END TEST")
print("=" * 70)

# Step 1: Register a new user
print("\n1️⃣ Registering new user...")
email = f"test_{int(time.time())}@test.com"
response = requests.post(
    f"{BASE_URL}/register",
    json={"email": email, "password": "test123"}
)

if response.status_code != 200:
    print(f"❌ Registration failed: {response.status_code}")
    print(response.text)
    exit(1)

token = response.json()['access_token']
payload = token.split('.')[1] + '=' * (4 - len(token.split('.')[1]) % 4)
user_id = json.loads(base64.b64decode(payload)).get('sub')

print(f"✅ User registered: {email}")
print(f"   User ID: {user_id}")

# Step 2: Send a general message
print("\n2️⃣ Sending general message: 'playing'...")
response = requests.post(
    f"{BASE_URL}/api/{user_id}/chat",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    json={"message": "playing"}
)

print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"   Response: {data.get('response', 'No response')[:100]}...")
else:
    print(f"   Error: {response.text}")

# Step 3: Add a task
print("\n3️⃣ Adding task: 'Add task: playing games'...")
response = requests.post(
    f"{BASE_URL}/api/{user_id}/chat",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    json={"message": "Add task: playing games"}
)

print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"   Response: {data.get('response', 'No response')}")
    if data.get('tool_calls'):
        print(f"   Tool calls: {len(data['tool_calls'])}")
        for call in data['tool_calls']:
            print(f"      - {call['tool_name']}: {call['arguments']}")
else:
    print(f"   Error: {response.text}")

# Step 4: List tasks via chat
print("\n4️⃣ Listing tasks via chat...")
response = requests.post(
    f"{BASE_URL}/api/{user_id}/chat",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    json={"message": "list tasks"}
)

print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"   Response: {data.get('response', 'No response')}")
else:
    print(f"   Error: {response.text}")

# Step 5: Get tasks via API
print("\n5️⃣ Getting tasks via API...")
response = requests.get(
    f"{BASE_URL}/api/{user_id}/tasks",
    headers={"Authorization": f"Bearer {token}"}
)

print(f"   Status: {response.status_code}")
if response.status_code == 200:
    tasks = response.json()
    print(f"   ✅ Found {len(tasks)} tasks:")
    for task in tasks:
        print(f"      - {task['title']} ({task['status']})")
else:
    print(f"   Error: {response.text}")

# Step 6: Check database directly
print("\n6️⃣ Checking database...")
import sqlite3
conn = sqlite3.connect("backend/todo_app_local.db")
cursor = conn.cursor()

# Try different UUID formats
cursor.execute("SELECT id, email FROM users")
all_users = cursor.fetchall()
print(f"   Total users in DB: {len(all_users)}")

# Find our user by email
cursor.execute("SELECT id, email FROM users WHERE email = ?", (email,))
user_row = cursor.fetchone()

if not user_row:
    # Try to find by converting UUID
    import uuid
    try:
        uuid_obj = uuid.UUID(user_id)
        # Try hex format (no dashes)
        cursor.execute("SELECT id, email FROM users WHERE id = ?", (uuid_obj.hex,))
        user_row = cursor.fetchone()
        
        if not user_row:
            # Try with dashes
            cursor.execute("SELECT id, email FROM users WHERE id = ?", (str(uuid_obj),))
            user_row = cursor.fetchone()
    except:
        pass

if user_row:
    print(f"   ✅ User in DB: {user_row[1]} (ID: {user_row[0]})")
    
    # Get tasks for this user
    db_user_id = user_row[0]
    cursor.execute("SELECT id, title, status, user_id FROM tasks WHERE user_id = ?", (db_user_id,))
    task_rows = cursor.fetchall()
    print(f"   ✅ Tasks in DB: {len(task_rows)}")
    for task_row in task_rows:
        print(f"      - {task_row[1]} ({task_row[2]}) [user: {task_row[3]}]")
else:
    print(f"   ❌ User not found in database")
    print(f"   Looking for: {email} or {user_id}")
    print(f"   Available users:")
    for u in all_users[:5]:
        print(f"      - {u[1]} (ID: {u[0]})")

conn.close()

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)
