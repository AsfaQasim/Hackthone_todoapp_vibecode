"""Debug why tasks are not showing in AI Tasks page"""
import requests
import json

BACKEND_URL = "http://localhost:8000"

print("=" * 80)
print("🔍 DEBUGGING AI TASKS ISSUE")
print("=" * 80)

# Step 1: Login
print("\n1️⃣ Logging in...")
try:
    response = requests.post(
        f"{BACKEND_URL}/login",
        json={"email": "asfaqasim145@gmail.com", "password": "test123"},
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        data = response.json()
        token = data.get("token") or data.get("access_token")
        user_id = data.get("user_id")
        
        print(f"   ✅ Login successful!")
        print(f"   User ID: {user_id}")
        print(f"   Token: {token[:30]}...")
    else:
        print(f"   ❌ Login failed: {response.status_code}")
        print(f"   Response: {response.text}")
        exit(1)
except Exception as e:
    print(f"   ❌ Login error: {e}")
    exit(1)

# Step 2: Get tasks from backend directly
print("\n2️⃣ Getting tasks from backend...")
try:
    response = requests.get(
        f"{BACKEND_URL}/api/{user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        tasks = response.json()
        print(f"   ✅ Backend returned {len(tasks)} tasks")
        
        if len(tasks) > 0:
            print(f"\n   📋 Tasks in backend:")
            for i, task in enumerate(tasks[:5], 1):
                print(f"      {i}. {task.get('title')} (Status: {task.get('status')})")
                print(f"         ID: {task.get('id')}")
                print(f"         User ID: {task.get('user_id')}")
        else:
            print(f"   ⚠️  No tasks found in backend!")
            print(f"   Let's create one...")
    else:
        print(f"   ❌ Backend returned error: {response.status_code}")
        print(f"   Response: {response.text}")
        
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Step 3: Create a test task
print("\n3️⃣ Creating a test task via chat...")
try:
    response = requests.post(
        f"{BACKEND_URL}/api/{user_id}/chat",
        json={"message": "add task: Debug test task"},
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Chat response: {data.get('response')}")
        
        if data.get('tool_calls'):
            for tool in data['tool_calls']:
                result = tool.get('result', {})
                if result.get('success'):
                    print(f"   ✅ Task created successfully!")
                    task_data = result.get('data', {})
                    print(f"      Task ID: {task_data.get('id')}")
                    print(f"      Title: {task_data.get('title')}")
    else:
        print(f"   ❌ Chat failed: {response.status_code}")
        print(f"   Response: {response.text[:500]}")
        
except Exception as e:
    print(f"   ❌ Error: {e}")

# Step 4: Get tasks again
print("\n4️⃣ Getting tasks again...")
try:
    response = requests.get(
        f"{BACKEND_URL}/api/{user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        tasks = response.json()
        print(f"   ✅ Backend now has {len(tasks)} tasks")
        
        if len(tasks) > 0:
            print(f"\n   📋 Latest tasks:")
            for i, task in enumerate(tasks[-3:], 1):
                print(f"      {i}. {task.get('title')}")
                print(f"         ID: {task.get('id')}")
                print(f"         User ID: {task.get('user_id')}")
                print(f"         Status: {task.get('status')}")
    else:
        print(f"   ❌ Error: {response.status_code}")
        
except Exception as e:
    print(f"   ❌ Error: {e}")

# Step 5: Test frontend API route
print("\n5️⃣ Testing frontend API route...")
try:
    response = requests.get(
        "http://localhost:3000/api/tasks",
        headers={"Authorization": f"Bearer {token}"},
        cookies={"auth_token": token}
    )
    
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        tasks = response.json()
        print(f"   ✅ Frontend API returned {len(tasks)} tasks")
        
        if len(tasks) > 0:
            print(f"\n   📋 Tasks from frontend API:")
            for i, task in enumerate(tasks[:3], 1):
                print(f"      {i}. {task.get('title')}")
        else:
            print(f"   ⚠️  Frontend API returned 0 tasks!")
            print(f"   This is the problem!")
    else:
        print(f"   ❌ Frontend API error: {response.status_code}")
        print(f"   Response: {response.text[:500]}")
        
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("📊 SUMMARY")
print("=" * 80)
print("\n✅ If backend has tasks but frontend API returns 0:")
print("   Problem: Frontend API route not connecting to backend properly")
print("   Solution: Check frontend/.env.local has NEXT_PUBLIC_API_URL=http://localhost:8000")
print("\n✅ If backend has 0 tasks:")
print("   Problem: Tasks not being created")
print("   Solution: Check backend logs for errors")
print("\n✅ If frontend API has tasks:")
print("   Problem: Frontend page not refreshing")
print("   Solution: Hard refresh browser (Ctrl+Shift+R)")
print("=" * 80)
