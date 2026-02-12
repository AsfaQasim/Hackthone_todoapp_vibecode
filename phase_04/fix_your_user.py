"""Fix for your specific user"""
import sqlite3
import uuid

YOUR_USER_ID = "65d85bae-6ae6-4f9d-be8c-d149a177f8fc"
YOUR_EMAIL = "asfaqasim145@gmail.com"

print("=" * 70)
print("FIXING YOUR USER")
print("=" * 70)

conn = sqlite3.connect("backend/todo_app_local.db")
cursor = conn.cursor()

# Check if user exists
cursor.execute("SELECT id, email FROM users WHERE id = ?", (YOUR_USER_ID,))
user = cursor.fetchone()

if user:
    print(f"\n✅ User already exists: {user[1]}")
else:
    print(f"\n❌ User not found, creating...")
    try:
        cursor.execute(
            "INSERT INTO users (id, email, name, created_at, updated_at) VALUES (?, ?, ?, datetime('now'), datetime('now'))",
            (YOUR_USER_ID, YOUR_EMAIL, YOUR_EMAIL.split('@')[0])
        )
        conn.commit()
        print(f"✅ User created!")
    except Exception as e:
        print(f"❌ Error: {e}")

# Create test tasks
print("\n📝 Creating test tasks...")
test_tasks = ["Eating", "Playing", "Shopping", "Coding", "Reading"]

for task_title in test_tasks:
    task_id = str(uuid.uuid4())
    try:
        cursor.execute(
            "INSERT INTO tasks (id, user_id, title, description, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, datetime('now'), datetime('now'))",
            (task_id, YOUR_USER_ID, task_title, "Test task", "pending")
        )
        print(f"   ✅ {task_title}")
    except Exception as e:
        print(f"   ❌ {task_title}: {e}")

conn.commit()

# Verify
print("\n🔍 Verifying...")
cursor.execute("SELECT id, title FROM tasks WHERE user_id = ?", (YOUR_USER_ID,))
tasks = cursor.fetchall()
print(f"✅ Total tasks: {len(tasks)}")
for task in tasks:
    print(f"   - {task[1]}")

conn.close()

print("\n" + "=" * 70)
print("DONE! Now refresh your general-task-execution page!")
print("=" * 70)
