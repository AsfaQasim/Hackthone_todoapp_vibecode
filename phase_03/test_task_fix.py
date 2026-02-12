"""Test script to verify task retrieval fix"""
import requests
import json

# Test configuration
BASE_URL = "http://localhost:8000"
USER_ID = "65d85bae-6ae6-4f9d-be8c-d149a177f8fc"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ4NWJhZS02YWU2LTRmOWQtYmU4Yy1kMTQ5YTE3N2Y4ZmMiLCJlbWFpbCI6ImFzZmFxYXNpbTE0NUBnbWFpbC5jb20iLCJ1c2VyX2VtYWlsIjoiYXNmYXFhc2ltMTQ1QGdtYWlsLmNvbSIsIm5hbWUiOiJhc2ZhcWFzaW0xNDUiLCJleHAiOjE3NzA0NTY0ODB9.RdzeeqqczHlZdSjyPvX_Rw40yN_bq_-BoF29r2b7Y8Q"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

print("=" * 70)
print("TESTING TASK RETRIEVAL FIX")
print("=" * 70)

# Test 1: List tasks
print("\n1️⃣ Testing GET /api/{user_id}/tasks")
response = requests.get(f"{BASE_URL}/api/{USER_ID}/tasks", headers=headers)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    tasks = response.json()
    print(f"✅ Found {len(tasks)} tasks")
    for i, task in enumerate(tasks[:3], 1):  # Show first 3 tasks
        print(f"   {i}. {task['title']} ({task['status']})")
    if len(tasks) > 3:
        print(f"   ... and {len(tasks) - 3} more")
else:
    print(f"❌ Error: {response.text}")

# Test 2: Create a new task
print("\n2️⃣ Testing POST /api/{user_id}/tasks")
new_task = {
    "title": "Test Task - Fix Verification",
    "description": "Testing the UUID fix",
    "status": "pending"
}
response = requests.post(f"{BASE_URL}/api/{USER_ID}/tasks", headers=headers, json=new_task)
print(f"Status: {response.status_code}")

if response.status_code == 200:
    task = response.json()
    print(f"✅ Created task: {task['title']}")
    print(f"   Task ID: {task['id']}")
    created_task_id = task['id']
else:
    print(f"❌ Error: {response.text}")
    created_task_id = None

# Test 3: Get specific task
if created_task_id:
    print(f"\n3️⃣ Testing GET /api/{user_id}/tasks/{created_task_id}")
    response = requests.get(f"{BASE_URL}/api/{USER_ID}/tasks/{created_task_id}", headers=headers)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        task = response.json()
        print(f"✅ Retrieved task: {task['title']}")
    else:
        print(f"❌ Error: {response.text}")

print("\n" + "=" * 70)
print("TEST COMPLETE")
print("=" * 70)
print("\n⚠️  IMPORTANT: Backend must be restarted for changes to take effect!")
print("Run: cd backend && uvicorn main:app --reload")
