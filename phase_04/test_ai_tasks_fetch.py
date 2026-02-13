"""Test AI tasks fetching with real authentication."""

import requests
import json

print("=" * 80)
print("🔍 TESTING AI TASKS FETCH")
print("=" * 80)

# Test credentials
TEST_EMAIL = "asfaqasim145@gmail.com"
TEST_PASSWORD = "123456"

# Backend URL
BACKEND_URL = "http://localhost:8000"

print(f"\n1️⃣ Logging in as {TEST_EMAIL}...")
print("-" * 80)

# Login to get token
login_response = requests.post(
    f"{BACKEND_URL}/login",
    json={
        "email": TEST_EMAIL,
        "password": TEST_PASSWORD
    }
)

print(f"Login status: {login_response.status_code}")

if login_response.status_code == 200:
    login_data = login_response.json()
    token = login_data.get("access_token")
    user_id = login_data.get("user", {}).get("id")
    
    print(f"✅ Login successful!")
    print(f"   User ID: {user_id}")
    print(f"   Token: {token[:30]}...")
    
    print(f"\n2️⃣ Fetching tasks from backend...")
    print("-" * 80)
    
    # Fetch tasks
    tasks_response = requests.get(
        f"{BACKEND_URL}/api/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    
    print(f"Tasks fetch status: {tasks_response.status_code}")
    
    if tasks_response.status_code == 200:
        tasks = tasks_response.json()
        print(f"✅ Fetched {len(tasks)} tasks")
        
        if tasks:
            print(f"\n📋 Tasks:")
            for i, task in enumerate(tasks, 1):
                print(f"\n   {i}. {task.get('title')}")
                print(f"      ID: {task.get('id')}")
                print(f"      Status: {task.get('status')}")
                print(f"      Description: {task.get('description', 'N/A')}")
                print(f"      Created: {task.get('created_at', 'N/A')}")
        else:
            print(f"\n⚠️ No tasks found for this user")
            
            print(f"\n3️⃣ Creating a test task...")
            print("-" * 80)
            
            # Create a test task
            create_response = requests.post(
                f"{BACKEND_URL}/api/tasks",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                json={
                    "title": "Test task from AI Tasks page",
                    "description": "Created via test script"
                }
            )
            
            print(f"Create task status: {create_response.status_code}")
            
            if create_response.status_code in [200, 201]:
                new_task = create_response.json()
                print(f"✅ Task created successfully!")
                print(f"   ID: {new_task.get('id')}")
                print(f"   Title: {new_task.get('title')}")
                
                # Fetch tasks again
                print(f"\n4️⃣ Fetching tasks again...")
                print("-" * 80)
                
                tasks_response2 = requests.get(
                    f"{BACKEND_URL}/api/tasks",
                    headers={
                        "Authorization": f"Bearer {token}"
                    }
                )
                
                if tasks_response2.status_code == 200:
                    tasks2 = tasks_response2.json()
                    print(f"✅ Now have {len(tasks2)} tasks")
                else:
                    print(f"❌ Failed to fetch tasks: {tasks_response2.status_code}")
            else:
                print(f"❌ Failed to create task: {create_response.status_code}")
                print(f"   Response: {create_response.text}")
    else:
        print(f"❌ Failed to fetch tasks: {tasks_response.status_code}")
        print(f"   Response: {tasks_response.text}")
else:
    print(f"❌ Login failed: {login_response.status_code}")
    print(f"   Response: {login_response.text}")

print(f"\n" + "=" * 80)
print("✅ TEST COMPLETE")
print("=" * 80)
