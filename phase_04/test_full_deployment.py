"""
Complete deployment test for both local and production environments
"""
import requests
import json

# Configuration
BACKEND_URL = "https://hackthone-todoapp-vibecode-nudz.vercel.app"
TEST_USER = {
    "email": "asfaqasim145@gmail.com",
    "password": "test123"  # Replace with actual password
}

print("=" * 80)
print("🚀 FULL DEPLOYMENT TEST")
print("=" * 80)

# Test 1: Backend Health Check
print("\n1️⃣ Testing Backend Health...")
try:
    response = requests.get(f"{BACKEND_URL}/health")
    if response.status_code == 200:
        print(f"   ✅ Backend is healthy: {response.json()}")
    else:
        print(f"   ❌ Backend health check failed: {response.status_code}")
except Exception as e:
    print(f"   ❌ Backend connection failed: {e}")

# Test 2: Backend Root Endpoint
print("\n2️⃣ Testing Backend Root...")
try:
    response = requests.get(BACKEND_URL)
    if response.status_code == 200:
        print(f"   ✅ Root endpoint working: {response.json()}")
    else:
        print(f"   ❌ Root endpoint failed: {response.status_code}")
except Exception as e:
    print(f"   ❌ Root endpoint error: {e}")

# Test 3: Login (to get auth token)
print("\n3️⃣ Testing Login...")
try:
    response = requests.post(
        f"{BACKEND_URL}/login",
        json=TEST_USER,
        headers={"Content-Type": "application/json"}
    )
    if response.status_code == 200:
        data = response.json()
        if "token" in data:
            token = data["token"]
            user_id = data.get("user_id")
            print(f"   ✅ Login successful!")
            print(f"   User ID: {user_id}")
            print(f"   Token: {token[:20]}...")
            
            # Test 4: Get Tasks
            print("\n4️⃣ Testing Get Tasks...")
            try:
                response = requests.get(
                    f"{BACKEND_URL}/api/{user_id}/tasks",
                    headers={"Authorization": f"Bearer {token}"}
                )
                if response.status_code == 200:
                    tasks = response.json()
                    print(f"   ✅ Tasks retrieved: {len(tasks)} tasks found")
                    for task in tasks[:3]:  # Show first 3 tasks
                        print(f"      - {task.get('title', 'No title')}")
                else:
                    print(f"   ❌ Get tasks failed: {response.status_code}")
                    print(f"   Response: {response.text}")
            except Exception as e:
                print(f"   ❌ Get tasks error: {e}")
            
            # Test 5: Create Task via Chat
            print("\n5️⃣ Testing Create Task via Chat...")
            try:
                response = requests.post(
                    f"{BACKEND_URL}/api/{user_id}/chat",
                    json={"message": "Add task: Test deployment task"},
                    headers={
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json"
                    }
                )
                if response.status_code == 200:
                    data = response.json()
                    print(f"   ✅ Chat response received")
                    print(f"   Response: {data.get('response', 'No response')[:100]}...")
                else:
                    print(f"   ❌ Chat failed: {response.status_code}")
                    print(f"   Response: {response.text[:200]}")
            except Exception as e:
                print(f"   ❌ Chat error: {e}")
        else:
            print(f"   ❌ Login response missing token: {data}")
    else:
        print(f"   ❌ Login failed: {response.status_code}")
        print(f"   Response: {response.text}")
except Exception as e:
    print(f"   ❌ Login error: {e}")

print("\n" + "=" * 80)
print("✅ DEPLOYMENT TEST COMPLETE")
print("=" * 80)
print("\n📝 Next Steps:")
print("1. Go to Vercel dashboard")
print("2. Add environment variable: NEXT_PUBLIC_API_URL = " + BACKEND_URL)
print("3. Redeploy frontend")
print("4. Test the deployed frontend URL")
print("=" * 80)
