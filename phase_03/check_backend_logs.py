"""Check if backend is running and test the chat endpoint"""
import requests
import json

BACKEND_URL = "http://localhost:8000"

print("=" * 80)
print("🔍 CHECKING BACKEND STATUS")
print("=" * 80)

# Test 1: Check if backend is running
print("\n1️⃣ Checking if backend is running...")
try:
    response = requests.get(f"{BACKEND_URL}/health", timeout=5)
    if response.status_code == 200:
        print(f"   ✅ Backend is running!")
        print(f"   Response: {response.json()}")
    else:
        print(f"   ❌ Backend returned: {response.status_code}")
except requests.exceptions.ConnectionError:
    print(f"   ❌ Backend is NOT running!")
    print(f"   Please start backend:")
    print(f"   cd backend")
    print(f"   python -m uvicorn main:app --reload")
    exit(1)
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Test 2: Try to login
print("\n2️⃣ Testing login...")
try:
    response = requests.post(
        f"{BACKEND_URL}/login",
        json={"email": "test@example.com", "password": "test123"},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        token = data.get("token") or data.get("access_token")
        user_id = data.get("user_id")
        
        if not token:
            print(f"   ❌ No token in response!")
            print(f"   Response: {data}")
            exit(1)
        
        if not user_id:
            print(f"   ⚠️  No user_id in response!")
            print(f"   Response: {data}")
            print(f"   Backend needs restart!")
            exit(1)
        
        print(f"   ✅ Login successful!")
        print(f"   User ID: {user_id}")
        print(f"   Token: {token[:30]}...")
        
        # Test 3: Try to create task via chat
        print("\n3️⃣ Testing chat endpoint...")
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/{user_id}/chat",
                json={"message": "add task: Test backend restart"},
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                }
            )
            
            print(f"   Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Chat response received!")
                print(f"   Response: {data.get('response')}")
                
                if data.get('tool_calls'):
                    print(f"   ✅ Task creation attempted!")
                    for tool in data['tool_calls']:
                        result = tool.get('result', {})
                        if result.get('success'):
                            print(f"   ✅ Task created successfully!")
                        else:
                            print(f"   ❌ Task creation failed!")
                            print(f"   Error: {result}")
                else:
                    print(f"   ⚠️  No tool calls in response")
            else:
                print(f"   ❌ Chat failed: {response.status_code}")
                print(f"   Response: {response.text[:500]}")
                
        except Exception as e:
            print(f"   ❌ Chat error: {e}")
            import traceback
            traceback.print_exc()
    else:
        print(f"   ❌ Login failed: {response.status_code}")
        print(f"   Response: {response.text}")
        
except Exception as e:
    print(f"   ❌ Login error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("✅ CHECK COMPLETE")
print("=" * 80)
print("\n📝 If you see 'Backend needs restart', do this:")
print("   1. Go to backend terminal")
print("   2. Press Ctrl+C")
print("   3. Run: python -m uvicorn main:app --reload")
print("=" * 80)
