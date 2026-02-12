"""Test with the correct user ID from database"""
import requests

BACKEND_URL = "http://localhost:8000"
CORRECT_USER_ID = "add60fd1-792f-4ab9-9a53-e2f859482c59"  # From database

print("=" * 80)
print("🧪 TESTING WITH CORRECT USER ID")
print("=" * 80)

# Step 1: Login to get token
print("\n1️⃣ Logging in...")
response = requests.post(
    f"{BACKEND_URL}/login",
    json={"email": "asfaqasim145@gmail.com", "password": "test123"}
)

if response.status_code == 200:
    data = response.json()
    token = data.get("token") or data.get("access_token")
    returned_user_id = data.get("user_id")
    
    print(f"   ✅ Login successful!")
    print(f"   Returned User ID: {returned_user_id}")
    print(f"   Expected User ID: {CORRECT_USER_ID}")
    
    if returned_user_id == CORRECT_USER_ID:
        print(f"   ✅ USER ID MATCHES! Backend restart worked!")
    else:
        print(f"   ❌ USER ID MISMATCH! Backend needs restart!")
        print(f"   Please restart backend:")
        print(f"   1. Go to backend terminal")
        print(f"   2. Press Ctrl+C")
        print(f"   3. Run: python -m uvicorn main:app --reload")
        exit(1)
    
    # Step 2: Get tasks
    print(f"\n2️⃣ Getting tasks for user {returned_user_id}...")
    response = requests.get(
        f"{BACKEND_URL}/api/{returned_user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        tasks = response.json()
        print(f"   ✅ Got {len(tasks)} tasks!")
        
        if len(tasks) > 0:
            print(f"\n   📋 Tasks:")
            for i, task in enumerate(tasks[:5], 1):
                print(f"      {i}. {task.get('title')} ({task.get('status')})")
        else:
            print(f"   ⚠️  No tasks found!")
    else:
        print(f"   ❌ Error: {response.status_code}")
        print(f"   Response: {response.text}")
else:
    print(f"   ❌ Login failed: {response.status_code}")
    print(f"   Response: {response.text}")

print("\n" + "=" * 80)
