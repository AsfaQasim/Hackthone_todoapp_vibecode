"""Simple database check"""
import sqlite3

# Check the database file
db_path = "backend/todo_app_local.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Users table:")
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
for user in users:
    print(f"  {user}")

print("\nTasks table:")
cursor.execute("SELECT * FROM tasks")
tasks = cursor.fetchall()
for task in tasks:
    print(f"  {task}")

conn.close()
