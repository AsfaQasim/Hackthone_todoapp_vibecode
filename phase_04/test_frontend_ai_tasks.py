"""Test the AI tasks endpoint with a real user token."""

import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 80)
print("🧪 TESTING AI TASKS ENDPOINT")
print("=" * 80)

# Step 1: Login to get a valid token
print("\n1. Logging in...")
login_response = requests.post(
    f"{BASE_URL}/api/auth/login",
    json={
        "email": "asfaqasim145@gmail.com",
        "password": "test123"  # You'll need to use the correct password
    }
)

if login_response.status_code == 200:
    login_data = login_response.json()
    token = login_data.get("access_token")
    print(f"✅ Login successful!")
    print(f"   Token: {token[:50]}...")
    
    # Step 2: Fetch tasks
    print("\n2. Fetching AI tasks...")
    tasks_response = requests.get(
        f"{BASE_URL}/api/tasks",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )
    
    print(f"   Status: {tasks_response.status_code}")
    
    if tasks_response.status_code == 200:
        tasks = tasks_response.json()
        print(f"✅ Tasks fetched successfully!")
        print(f"   Found {len(tasks)} tasks")
        
        if tasks:
            print("\n   Tasks:")
            for task in tasks[:5]:  # Show first 5
                print(f"   - {task.get('title')} ({task.get('status')})")
        else:
            print("   No tasks found")
    else:
        print(f"❌ Failed to fetch tasks")
        print(f"   Response: {tasks_response.text}")
        
else:
    print(f"❌ Login failed: {login_response.status_code}")
    print(f"   Response: {login_response.text}")
    print("\n💡 Try creating a test user first:")
    print("   python create_test_user.py")

print("\n" + "=" * 80)
