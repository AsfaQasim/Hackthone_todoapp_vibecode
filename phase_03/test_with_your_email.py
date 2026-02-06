"""Test with your actual email"""
import requests
import json
import base64

BASE_URL = "http://localhost:8000"
YOUR_EMAIL = "asfaqasim145@gmail.com"

print("=" * 70)
print(f"TESTING WITH YOUR EMAIL: {YOUR_EMAIL}")
print("=" * 70)

# Step 1: Register/Login
print("\n1️⃣ Registering/Login...")
response = requests.post(
    f"{BASE_URL}/register",
    json={"email": YOUR_EMAIL, "password": "test123"}
)

if response.status_code != 200:
    print(f"❌ Registration failed: {response.status_code}")
    print(response.text)
    exit(1)

token = response.json()['access_token']
payload = token.split('.')[1] + '=' * (4 - len(token.split('.')[1]) % 4)
user_id = json.loads(base64.b64decode(payload)).get('sub')

print(f"✅ Token received")
print(f"   User ID: {user_id}")

# Step 2: Add a task via chat
print("\n2️⃣ Adding task via chat: 'Add task: eating'...")
response = requests.post(
    f"{BASE_URL}/api/{user_id}/chat",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    json={"message": "Add task: eating"}
)

print(f"   Status: {response.status_code}")
if response.status_code == 200:
    data = response.json()
    print(f"   Response: {data.get('response', '')[:100]}")
    if data.get('tool_calls'):
        print(f"   ✅ Task created!")
    else:
        print(f"   ❌ No task created")
else:
    print(f"   ❌ Error: {response.text}")

# Step 3: List tasks via API
print("\n3️⃣ Fetching tasks via API...")
response = requests.get(
    f"{BASE_URL}/api/{user_id}/tasks",
    headers={"Authorization": f"Bearer {token}"}
)

print(f"   Status: {response.status_code}")
if response.status_code == 200:
    tasks = response.json()
    print(f"   ✅ Found {len(tasks)} tasks")
    for task in tasks:
        print(f"      - {task['title']} ({task['status']})")
else:
    print(f"   ❌ Error: {response.text}")

# Step 4: Check database
print("\n4️⃣ Checking database...")
import sqlite3
conn = sqlite3.connect("backend/todo_app_local.db")
cursor = conn.cursor()

cursor.execute("SELECT id, email FROM users WHERE email = ?", (YOUR_EMAIL,))
user_row = cursor.fetchone()

if user_row:
    print(f"   ✅ User in DB: {user_row[1]}")
    cursor.execute("SELECT id, title, status FROM tasks WHERE user_id = ?", (user_row[0],))
    tasks = cursor.fetchall()
    print(f"   ✅ Tasks in DB: {len(tasks)}")
    for task in tasks:
        print(f"      - {task[1]} ({task[2]})")
else:
    print(f"   ❌ User not in database")

conn.close()

print("\n" + "=" * 70)
print("SUMMARY:")
print("If tasks show in API but not in database, backend is using memory")
print("If tasks don't show anywhere, chat is not working")
print("=" * 70)
