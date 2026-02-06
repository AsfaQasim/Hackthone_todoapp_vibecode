"""Debug frontend-backend task sync"""
import requests
import json

# Use your actual user email
USER_EMAIL = "asfaqasim145@gmail.com"

print("=" * 70)
print("DEBUGGING FRONTEND-BACKEND TASK SYNC")
print("=" * 70)

# Step 1: Check if user exists in backend database
print("\n1️⃣ Checking backend database...")
import sqlite3
conn = sqlite3.connect("backend/todo_app_local.db")
cursor = conn.cursor()

cursor.execute("SELECT id, email FROM users WHERE email = ?", (USER_EMAIL,))
user_row = cursor.fetchone()

if user_row:
    user_id = user_row[0]
    print(f"   ✅ User found: {user_row[1]}")
    print(f"   User ID: {user_id}")
    
    # Check tasks for this user
    cursor.execute("SELECT id, title, status, user_id FROM tasks WHERE user_id = ?", (user_id,))
    tasks = cursor.fetchall()
    print(f"\n   Tasks in backend DB: {len(tasks)}")
    for task in tasks:
        print(f"      - {task[1]} ({task[2]}) [user_id: {task[3]}]")
else:
    print(f"   ❌ User not found: {USER_EMAIL}")
    print("\n   All users in database:")
    cursor.execute("SELECT id, email FROM users")
    all_users = cursor.fetchall()
    for u in all_users[:10]:
        print(f"      - {u[1]} (ID: {u[0]})")

conn.close()

# Step 2: Try to fetch via backend API (need token)
print("\n2️⃣ To test backend API, you need to:")
print("   1. Login to frontend")
print("   2. Open browser console (F12)")
print("   3. Run: document.cookie")
print("   4. Copy the auth_token value")
print("   5. Run this script with token")

print("\n" + "=" * 70)
print("NEXT STEPS:")
print("=" * 70)
print("1. Check if your user email matches exactly")
print("2. Check browser console for errors")
print("3. Check backend logs when loading general-task-execution page")
print("=" * 70)
