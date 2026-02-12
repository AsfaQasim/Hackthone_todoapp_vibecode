"""Test backend directly to see what's happening"""
import requests
import json

BACKEND_URL = "http://localhost:8000"

print("=" * 80)
print("🔍 TESTING BACKEND DIRECTLY")
print("=" * 80)

# Test 1: Health check
print("\n1️⃣ Health check...")
try:
    response = requests.get(f"{BACKEND_URL}/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except Exception as e:
    print(f"   ❌ Error: {e}")
    print(f"   Backend is not running!")
    exit(1)

# Test 2: Login with detailed logging
print("\n2️⃣ Login test...")
try:
    response = requests.post(
        f"{BACKEND_URL}/login",
        json={"email": "asfaqasim145@gmail.com", "password": "test123"},
        headers={"Content-Type": "application/json"}
    )
    
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"   Response: {json.dumps(data, indent=2)}")
        
        user_id = data.get("user_id")
        print(f"\n   User ID: {user_id}")
        print(f"   Expected: add60fd1-792f-4ab9-9a53-e2f859482c59")
        
        if user_id == "add60fd1-792f-4ab9-9a53-e2f859482c59":
            print(f"   ✅ CORRECT USER ID!")
        else:
            print(f"   ❌ WRONG USER ID!")
            print(f"\n   🔍 Debugging:")
            print(f"   - Backend file has correct code")
            print(f"   - But backend is returning wrong user ID")
            print(f"   - This means backend is NOT reloading")
            print(f"\n   💡 Solution:")
            print(f"   1. Stop backend completely (Ctrl+C)")
            print(f"   2. Close the terminal")
            print(f"   3. Open NEW terminal")
            print(f"   4. cd backend")
            print(f"   5. python -m uvicorn main:app --reload")
    else:
        print(f"   ❌ Login failed: {response.text}")
        
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
