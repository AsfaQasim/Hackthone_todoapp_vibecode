"""Test the simplified tasks endpoint."""

import requests
import json

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_EMAIL = "asfaqasim145@gmail.com"
TEST_PASSWORD = "test123"

def test_tasks_flow():
    """Test the complete tasks flow."""
    
    print("=" * 60)
    print("🧪 Testing Tasks Endpoint")
    print("=" * 60)
    
    # Step 1: Login to get token
    print("\n1️⃣ Logging in...")
    login_response = requests.post(
        f"{BASE_URL}/login",
        json={
            "email": TEST_EMAIL,
            "password": TEST_PASSWORD
        }
    )
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(login_response.text)
        return
    
    login_data = login_response.json()
    token = login_data.get("access_token")
    user_id = login_data.get("user", {}).get("id")
    
    print(f"✅ Login successful!")
    print(f"   User ID: {user_id}")
    print(f"   Token: {token[:20]}...")
    
    # Step 2: Create a task via chat
    print("\n2️⃣ Creating task via chat...")
    chat_response = requests.post(
        f"{BASE_URL}/api/{user_id}/chat",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "message": "Add task: Test task from endpoint test"
        }
    )
    
    if chat_response.status_code != 200:
        print(f"❌ Chat failed: {chat_response.status_code}")
        print(chat_response.text)
        return
    
    chat_data = chat_response.json()
    print(f"✅ Chat response:")
    print(f"   Response: {chat_data.get('response')}")
    print(f"   Tool calls: {len(chat_data.get('tool_calls', []))}")
    
    # Step 3: Fetch tasks using simplified endpoint
    print("\n3️⃣ Fetching tasks from /api/tasks...")
    tasks_response = requests.get(
        f"{BASE_URL}/api/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if tasks_response.status_code != 200:
        print(f"❌ Fetch tasks failed: {tasks_response.status_code}")
        print(tasks_response.text)
        return
    
    tasks = tasks_response.json()
    print(f"✅ Tasks fetched successfully!")
    print(f"   Total tasks: {len(tasks)}")
    
    if tasks:
        print("\n📋 Tasks:")
        for i, task in enumerate(tasks[:5], 1):
            print(f"   {i}. {task.get('title')} ({task.get('status')})")
    
    # Step 4: Create another task directly via tasks endpoint
    print("\n4️⃣ Creating task via /api/tasks...")
    create_response = requests.post(
        f"{BASE_URL}/api/tasks",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "title": "Direct task creation test",
            "description": "Created directly via tasks endpoint"
        }
    )
    
    if create_response.status_code != 200:
        print(f"❌ Create task failed: {create_response.status_code}")
        print(create_response.text)
        return
    
    new_task = create_response.json()
    print(f"✅ Task created successfully!")
    print(f"   ID: {new_task.get('id')}")
    print(f"   Title: {new_task.get('title')}")
    
    # Step 5: Fetch tasks again to verify
    print("\n5️⃣ Fetching tasks again...")
    tasks_response2 = requests.get(
        f"{BASE_URL}/api/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if tasks_response2.status_code == 200:
        tasks2 = tasks_response2.json()
        print(f"✅ Tasks fetched successfully!")
        print(f"   Total tasks: {len(tasks2)}")
        print(f"   New task count: {len(tasks2) - len(tasks)}")
    
    print("\n" + "=" * 60)
    print("✅ All tests passed!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        test_tasks_flow()
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
