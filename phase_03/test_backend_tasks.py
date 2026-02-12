"""Test backend tasks endpoint"""
import requests

print("=" * 80)
print("🧪 TESTING BACKEND TASKS ENDPOINT")
print("=" * 80)

# Test 1: Check backend health
print("\n1️⃣ Testing backend health...")
try:
    response = requests.get("http://localhost:8000/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Get tasks from backend
print("\n2️⃣ Testing /api/my-tasks endpoint...")
try:
    response = requests.get("http://localhost:8000/api/my-tasks")
    print(f"Status: {response.status_code}")
    tasks = response.json()
    print(f"Tasks count: {len(tasks)}")
    
    if tasks:
        print("\n📋 Tasks found:")
        for task in tasks:
            print(f"  - {task['title']} (ID: {task['id'][:8]}..., Status: {task['status']})")
    else:
        print("⚠️ No tasks found!")
        
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Login and get token
print("\n3️⃣ Testing login...")
try:
    response = requests.post(
        "http://localhost:8000/login",
        json={
            "email": "asfaqasim145@gmail.com",
            "password": "test123"
        }
    )
    print(f"Status: {response.status_code}")
    if response.ok:
        data = response.json()
        print(f"✅ Login successful!")
        print(f"User ID: {data.get('user_id')}")
        print(f"Token: {data.get('token')[:20]}...")
    else:
        print(f"❌ Login failed: {response.text}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 80)
