"""Check UUID format in database"""
import sqlite3

conn = sqlite3.connect("backend/todo_app_local.db")
cursor = conn.cursor()

print("Users:")
cursor.execute("SELECT id, email, typeof(id) FROM users LIMIT 5")
for row in cursor.fetchall():
    print(f"  ID: {row[0]} | Email: {row[1]} | Type: {row[2]}")

print("\nTasks:")
cursor.execute("SELECT id, user_id, title, typeof(user_id) FROM tasks LIMIT 5")
for row in cursor.fetchall():
    print(f"  Task: {row[2]} | User ID: {row[1]} | Type: {row[3]}")

print("\nChecking specific user:")
user_id = "65d85bae-6ae6-4f9d-be8c-d149a177f8fc"
cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ?", (user_id,))
count = cursor.fetchone()[0]
print(f"Tasks for {user_id}: {count}")

# Try without dashes
user_id_no_dash = user_id.replace('-', '')
cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ?", (user_id_no_dash,))
count = cursor.fetchone()[0]
print(f"Tasks for {user_id_no_dash}: {count}")

# Try as BLOB
import uuid
user_uuid = uuid.UUID(user_id)
cursor.execute("SELECT COUNT(*) FROM tasks WHERE user_id = ?", (user_uuid.bytes,))
count = cursor.fetchone()[0]
print(f"Tasks for UUID bytes: {count}")

conn.close()
