"""Automatic fix for everything"""
import sqlite3
import uuid
import requests
import json
import base64

print("=" * 70)
print("AUTOMATIC FIX - CREATING USER AND TASKS IN DATABASE")
print("=" * 70)

YOUR_EMAIL = "asfaqasim145@gmail.com"

# Step 1: Create user in database
print("\n1️⃣ Creating user in backend database...")
conn = sqlite3.connect("backend/todo_app_local.db")
cursor = conn.cursor()

# Check if user exists
cursor.execute("SELECT id FROM users WHERE email = ?", (YOUR_EMAIL,))
existing = cursor.fetchone()

if existing:
    user_id = existing[0]
    print(f"   ✅ User already exists: {user_id}")
else:
    user_id = str(uuid.uuid4())
    try:
        cursor.execute(
            "INSERT INTO users (id, email, name, created_at, updated_at) VALUES (?, ?, ?, datetime('now'), datetime('now'))",
            (user_id, YOUR_EMAIL, YOUR_EMAIL.split('@')[0])
        )
        conn.commit()
        print(f"   ✅ User created: {user_id}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        conn.close()
        exit(1)

# Step 2: Create test tasks
print("\n2️⃣ Creating test tasks...")
test_tasks = ["Eating", "Playing", "Shopping"]

for task_title in test_tasks:
    task_id = str(uuid.uuid4())
    try:
        cursor.execute(
            "INSERT INTO tasks (id, user_id, title, description, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, datetime('now'), datetime('now'))",
            (task_id, user_id, task_title, "Created by auto-fix", "pending")
        )
        print(f"   ✅ Task created: {task_title}")
    except Exception as e:
        print(f"   ❌ Error creating {task_title}: {e}")

conn.commit()
conn.close()

# Step 3: Verify
print("\n3️⃣ Verifying database...")
conn = sqlite3.connect("backend/todo_app_local.db")
cursor = conn.cursor()

cursor.execute("SELECT id, email FROM users WHERE email = ?", (YOUR_EMAIL,))
user = cursor.fetchone()
print(f"   User: {user[1]} (ID: {user[0]})")

cursor.execute("SELECT id, title FROM tasks WHERE user_id = ?", (user[0],))
tasks = cursor.fetchall()
print(f"   Tasks: {len(tasks)}")
for task in tasks:
    print(f"      - {task[1]}")

conn.close()

# Step 4: Create JWT token for this user
print("\n4️⃣ Creating JWT token...")
import jwt
from datetime import datetime, timedelta

SECRET_KEY = "dea0238a9436145d14499ff6aeddb80870c4738f7268efec87b7acdff0589e066"
token_data = {
    "sub": user_id,
    "email": YOUR_EMAIL,
    "user_email": YOUR_EMAIL,
    "name": YOUR_EMAIL.split('@')[0],
    "exp": datetime.utcnow() + timedelta(days=1)
}

token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")
print(f"   Token created: {token[:50]}...")

# Step 5: Test API
print("\n5️⃣ Testing backend API...")
response = requests.get(
    f"http://localhost:8000/api/{user_id}/tasks",
    headers={"Authorization": f"Bearer {token}"}
)

if response.status_code == 200:
    api_tasks = response.json()
    print(f"   ✅ API returned {len(api_tasks)} tasks")
else:
    print(f"   ❌ API error: {response.status_code}")

print("\n" + "=" * 70)
print("DONE! Now:")
print("1. Copy this token and use it in browser:")
print(f"\n   {token}\n")
print("2. In browser console, run:")
print(f"   document.cookie = 'auth_token={token}; path=/;'")
print("3. Refresh general-task-execution page")
print("4. Tasks should appear!")
print("=" * 70)
