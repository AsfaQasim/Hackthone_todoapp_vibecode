"""Test backend directly with your user ID"""
import requests

USER_ID = "65d85bae-6ae6-4f9d-be8c-d149a177f8fc"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ4NWJhZS02YWU2LTRmOWQtYmU4Yy1kMTQ5YTE3N2Y4ZmMiLCJlbWFpbCI6ImFzZmFxYXNpbTE0NUBnbWFpbC5jb20iLCJ1c2VyX2VtYWlsIjoiYXNmYXFhc2ltMTQ1QGdtYWlsLmNvbSIsIm5hbWUiOiJhc2ZhcWFzaW0xNDUiLCJleHAiOjE3NzA0NTY0ODB9.RdzeeqqczHlZdSjyPvX_Rw40yN_bq_-BoF29r2b7Y8Q"

print("Testing backend API directly...")
print(f"User ID: {USER_ID}")

response = requests.get(
    f"http://localhost:8000/api/{USER_ID}/tasks",
    headers={"Authorization": f"Bearer {TOKEN}"}
)

print(f"\nStatus: {response.status_code}")
print(f"Response: {response.text}")

if response.status_code == 200:
    tasks = response.json()
    print(f"\nTasks: {len(tasks)}")
    for task in tasks:
        print(f"  - {task}")

# Also check database
print("\n" + "=" * 70)
print("Checking database...")
import sqlite3
conn = sqlite3.connect("backend/todo_app_local.db")
cursor = conn.cursor()

cursor.execute("SELECT id, title FROM tasks WHERE user_id = ?", (USER_ID,))
tasks = cursor.fetchall()
print(f"Tasks in DB: {len(tasks)}")
for task in tasks:
    print(f"  - {task[1]} (ID: {task[0]})")

conn.close()
