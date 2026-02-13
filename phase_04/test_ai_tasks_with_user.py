"""Test AI tasks endpoint with the actual user from the error message."""

import requests
import json

BASE_URL = "http://localhost:8000"
USER_EMAIL = "asfaqasim145@gmail.com"

print("=" * 80)
print("🧪 TESTING AI TASKS FOR USER:", USER_EMAIL)
print("=" * 80)

# First, let's check if this user exists in the database
print("\n1. Checking if user exists...")
print("   (We'll try to login, if it fails, we'll create the user)")

# Try to login
login_response = requests.post(
    f"{BASE_URL}/login",
    json={
        "email": USER_EMAIL,
        "password": "password123"  # Common test password
    }
)

token = None

if login_response.status_code == 200:
    data = login_response.json()
    token = data.get("access_token") or data.get("token")
    print(f"✅ Login successful!")
    print(f"   Token: {token[:50] if token else 'NO TOKEN'}...")
elif login_response.status_code == 401:
    print(f"❌ Login failed: Wrong password")
    print(f"   Try these passwords: password123, test123, Test@123")
    print(f"\n💡 Or create a new user:")
    print(f"   POST {BASE_URL}/register")
    print(f"   Body: {{'email': '{USER_EMAIL}', 'password': 'your_password'}}")
else:
    print(f"❌ Login endpoint error: {login_response.status_code}")
    print(f"   Response: {login_response.text}")

# If we have a token, try to fetch tasks
if token:
    print("\n2. Fetching AI tasks...")
    tasks_response = requests.get(
        f"{BASE_URL}/api/tasks",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )
    
    print(f"   Status: {tasks_response.status_code}")
    print(f"   Headers: {dict(tasks_response.headers)}")
    
    if tasks_response.status_code == 200:
        tasks = tasks_response.json()
        print(f"✅ Tasks fetched successfully!")
        print(f"   Found {len(tasks)} tasks")
        
        if tasks:
            print("\n   Your tasks:")
            for i, task in enumerate(tasks[:10], 1):
                print(f"   {i}. {task.get('title')} - {task.get('status')}")
        else:
            print("\n   No tasks found. Create some using the AI Assistant!")
    else:
        print(f"❌ Failed to fetch tasks")
        print(f"   Response: {tasks_response.text}")
        
        if tasks_response.status_code == 401:
            print("\n💡 Token might be invalid or expired")
            print("   Try logging in again from the frontend")
else:
    print("\n⚠️ Cannot test tasks endpoint without a valid token")
    print("\n📝 NEXT STEPS:")
    print("   1. Make sure you can login from the frontend")
    print("   2. Check browser cookies for 'auth_token'")
    print("   3. Copy that token and test with:")
    print(f"      curl -H 'Authorization: Bearer YOUR_TOKEN' {BASE_URL}/api/tasks")

print("\n" + "=" * 80)
