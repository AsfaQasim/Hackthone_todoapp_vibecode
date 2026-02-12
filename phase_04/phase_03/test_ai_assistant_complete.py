"""Complete test of AI Assistant functionality - creates a test user and verifies task creation."""

import requests
import json
import time

BACKEND_URL = "http://localhost:8000"

def test_complete_flow():
    """Test the complete flow: register -> login -> chat -> verify tasks."""
    
    print("=" * 70)
    print("COMPLETE AI ASSISTANT TEST")
    print("=" * 70)
    
    # Generate unique test user
    timestamp = int(time.time())
    test_email = f"test_user_{timestamp}@example.com"
    test_password = "testpass123"
    
    print(f"\n1. Creating test user: {test_email}")
    print("-" * 70)
    
    # Register
    try:
        response = requests.post(
            f"{BACKEND_URL}/register",
            json={"email": test_email, "password": test_password}
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            print(f"✅ User registered successfully")
            print(f"   Token: {token[:30]}...")
        else:
            print(f"❌ Registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return
    
    # Decode token to get user ID
    try:
        import base64
        payload = token.split('.')[1]
        # Add padding if needed
        payload += '=' * (4 - len(payload) % 4)
        decoded = json.loads(base64.b64decode(payload))
        user_id = decoded.get('sub') or decoded.get('userId') or decoded.get('user_id')
        print(f"   User ID: {user_id}")
    except Exception as e:
        print(f"⚠️ Could not decode token: {e}")
        user_id = "unknown"
    
    # Test chat endpoint with task creation
    print(f"\n2. Testing AI Assistant - Creating tasks via chat")
    print("-" * 70)
    
    test_messages = [
        "Add a task: Complete project documentation",
        "Create a task to review code changes",
        "Add task: Schedule team meeting for next week"
    ]
    
    created_tasks = []
    
    for i, message in enumerate(test_messages, 1):
        print(f"\n   Test {i}/3: '{message}'")
        try:
            response = requests.post(
                f"{BACKEND_URL}/api/{user_id}/chat",
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json"
                },
                json={
                    "message": message,
                    "conversation_id": None
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Handle both response formats
                if 'data' in data:
                    actual_data = data['data']
                else:
                    actual_data = data
                
                print(f"   ✅ AI responded")
                print(f"      Response: {actual_data.get('response', '')[:80]}...")
                
                tool_calls = actual_data.get('tool_calls', [])
                if tool_calls:
                    print(f"      Tool calls: {len(tool_calls)}")
                    for call in tool_calls:
                        tool_name = call.get('tool_name')
                        result = call.get('result', {})
                        success = result.get('success', False)
                        message_text = result.get('message', '')
                        
                        print(f"        - {tool_name}: {'✅' if success else '❌'} {message_text}")
                        
                        if success and tool_name == 'add_task':
                            task_data = result.get('data', {})
                            if task_data:
                                created_tasks.append(task_data)
                else:
                    print(f"      ⚠️ No tool calls made")
            else:
                print(f"   ❌ Chat failed: {response.status_code}")
                print(f"      Response: {response.text[:200]}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        
        time.sleep(1)  # Small delay between requests
    
    # Verify tasks were created
    print(f"\n3. Verifying tasks in database")
    print("-" * 70)
    
    try:
        response = requests.get(
            f"{BACKEND_URL}/api/{user_id}/tasks",
            headers={"Authorization": f"Bearer {token}"}
        )
        
        if response.status_code == 200:
            tasks = response.json()
            print(f"✅ Tasks retrieved successfully")
            print(f"   Total tasks: {len(tasks)}")
            
            if tasks:
                print(f"\n   Tasks in database:")
                for task in tasks:
                    print(f"     - {task.get('title')} ({task.get('status')})")
                    print(f"       ID: {task.get('id')}")
            else:
                print(f"   ⚠️ No tasks found in database")
        else:
            print(f"❌ Failed to retrieve tasks: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error retrieving tasks: {e}")
    
    # Summary
    print(f"\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Test user: {test_email}")
    print(f"User ID: {user_id}")
    print(f"Messages sent: {len(test_messages)}")
    print(f"Tasks created via AI: {len(created_tasks)}")
    print(f"Tasks in database: {len(tasks) if 'tasks' in locals() else 0}")
    
    if len(created_tasks) > 0 and len(tasks) > 0:
        print(f"\n✅ AI ASSISTANT IS WORKING CORRECTLY!")
        print(f"   - Tasks are being created via chat")
        print(f"   - Tasks are being saved to database")
        print(f"   - Tasks can be retrieved successfully")
    else:
        print(f"\n⚠️ SOME ISSUES DETECTED")
        if len(created_tasks) == 0:
            print(f"   - AI is not creating tasks (check OpenAI API key)")
        if len(tasks) == 0:
            print(f"   - Tasks are not being saved to database")
    
    print("=" * 70)

if __name__ == "__main__":
    test_complete_flow()
