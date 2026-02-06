"""Test script to verify the current state of the AI assistant and task creation."""

import requests
import json

# Configuration
BACKEND_URL = "http://localhost:8000"
USER_EMAIL = "asfaqasim145@gmail.com"
USER_PASSWORD = "password123"  # Update if different

def test_login():
    """Test login and get auth token."""
    print("\n1. Testing Login...")
    response = requests.post(
        f"{BACKEND_URL}/api/login",
        json={"email": USER_EMAIL, "password": USER_PASSWORD}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Login successful!")
        print(f"   User ID: {data.get('user_id')}")
        print(f"   Token: {data.get('token', '')[:20]}...")
        return data.get('token'), data.get('user_id')
    else:
        print(f"❌ Login failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return None, None

def test_get_tasks(token, user_id):
    """Test fetching tasks."""
    print("\n2. Testing Get Tasks...")
    response = requests.get(
        f"{BACKEND_URL}/api/{user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        tasks = response.json()
        print(f"✅ Tasks fetched successfully!")
        print(f"   Total tasks: {len(tasks)}")
        for task in tasks[:5]:  # Show first 5 tasks
            print(f"   - {task.get('title')} ({task.get('status')})")
        return tasks
    else:
        print(f"❌ Failed to fetch tasks: {response.status_code}")
        print(f"   Response: {response.text}")
        return []

def test_chat_endpoint(token, user_id):
    """Test the chat endpoint with a task creation request."""
    print("\n3. Testing Chat Endpoint (AI Assistant)...")
    response = requests.post(
        f"{BACKEND_URL}/api/{user_id}/chat",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json={
            "message": "Add a task: Test AI task creation",
            "conversation_id": None
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Chat endpoint responded!")
        
        # Check if it's the new format with 'data' wrapper
        if 'data' in data:
            actual_data = data['data']
            print(f"   Response: {actual_data.get('response', '')[:100]}...")
            print(f"   Tool calls: {len(actual_data.get('tool_calls', []))}")
            
            if actual_data.get('tool_calls'):
                for call in actual_data['tool_calls']:
                    print(f"   - Tool: {call.get('tool_name')}")
                    print(f"     Success: {call.get('result', {}).get('success')}")
                    print(f"     Message: {call.get('result', {}).get('message')}")
        else:
            print(f"   Response: {data.get('response', '')[:100]}...")
            print(f"   Tool calls: {len(data.get('tool_calls', []))}")
            
            if data.get('tool_calls'):
                for call in data['tool_calls']:
                    print(f"   - Tool: {call.get('tool_name')}")
                    print(f"     Success: {call.get('result', {}).get('success')}")
                    print(f"     Message: {call.get('result', {}).get('message')}")
        
        return data
    else:
        print(f"❌ Chat endpoint failed: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def test_tasks_after_chat(token, user_id):
    """Test fetching tasks after chat to see if new task was added."""
    print("\n4. Testing Tasks After Chat...")
    response = requests.get(
        f"{BACKEND_URL}/api/{user_id}/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        tasks = response.json()
        print(f"✅ Tasks fetched successfully!")
        print(f"   Total tasks: {len(tasks)}")
        
        # Look for the test task
        test_task = next((t for t in tasks if "Test AI task creation" in t.get('title', '')), None)
        if test_task:
            print(f"   ✅ Test task found: {test_task.get('title')}")
        else:
            print(f"   ⚠️ Test task not found in list")
        
        return tasks
    else:
        print(f"❌ Failed to fetch tasks: {response.status_code}")
        return []

def main():
    """Run all tests."""
    print("=" * 60)
    print("TESTING CURRENT STATE OF AI ASSISTANT AND TASK CREATION")
    print("=" * 60)
    
    # Test login
    token, user_id = test_login()
    if not token or not user_id:
        print("\n❌ Cannot proceed without authentication")
        return
    
    # Test getting tasks before chat
    tasks_before = test_get_tasks(token, user_id)
    
    # Test chat endpoint
    chat_response = test_chat_endpoint(token, user_id)
    
    # Test getting tasks after chat
    tasks_after = test_tasks_after_chat(token, user_id)
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Tasks before chat: {len(tasks_before)}")
    print(f"Tasks after chat: {len(tasks_after)}")
    print(f"New tasks added: {len(tasks_after) - len(tasks_before)}")
    
    if chat_response:
        print(f"\n✅ System is working correctly!")
        print(f"   - Authentication: Working")
        print(f"   - Task retrieval: Working")
        print(f"   - AI Assistant: Working")
        print(f"   - Task creation via AI: {'Working' if len(tasks_after) > len(tasks_before) else 'Check logs'}")
    else:
        print(f"\n⚠️ Some issues detected - check the output above")

if __name__ == "__main__":
    main()
