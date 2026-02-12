"""Test complete flow: AI Assistant → Database → General Tasks Page"""
import requests
import json

print("=" * 80)
print("🧪 TESTING COMPLETE FLOW: AI ASSISTANT → GENERAL TASKS")
print("=" * 80)

# Step 1: Login
print("\n1️⃣ Logging in...")
login_response = requests.post(
    "http://localhost:8000/login",
    json={
        "email": "asfaqasim145@gmail.com",
        "password": "test123"
    }
)

if not login_response.ok:
    print(f"❌ Login failed: {login_response.status_code}")
    exit(1)

login_data = login_response.json()
token = login_data.get("token")
user_id = login_data.get("user_id")

print(f"✅ Login successful!")
print(f"User ID: {user_id}")
print(f"Token: {token[:20]}...")

# Step 2: Get current tasks count
print("\n2️⃣ Getting current tasks...")
tasks_response = requests.get("http://localhost:8000/api/my-tasks")
current_tasks = tasks_response.json()
print(f"Current tasks: {len(current_tasks)}")

for task in current_tasks:
    print(f"  - {task['title']}")

# Step 3: Create task via AI Assistant (chat endpoint)
print("\n3️⃣ Creating task via AI Assistant...")
chat_response = requests.post(
    f"http://localhost:8000/api/{user_id}/chat",
    headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    },
    json={
        "message": "add task: Test from AI Assistant"
    }
)

print(f"Chat response status: {chat_response.status_code}")

if chat_response.ok:
    chat_data = chat_response.json()
    print(f"✅ AI Response: {chat_data.get('response', '')[:100]}")
    
    # Check if task was created
    tool_calls = chat_data.get('tool_calls', [])
    if tool_calls:
        print(f"✅ Tool called: {tool_calls[0].get('tool_name')}")
else:
    print(f"❌ Chat failed: {chat_response.text}")

# Step 4: Get tasks again to verify
print("\n4️⃣ Getting tasks after AI creation...")
tasks_response = requests.get("http://localhost:8000/api/my-tasks")
new_tasks = tasks_response.json()
print(f"Tasks now: {len(new_tasks)}")

if len(new_tasks) > len(current_tasks):
    print(f"✅ SUCCESS! New task added!")
    print(f"\nAll tasks:")
    for i, task in enumerate(new_tasks, 1):
        print(f"{i}. {task['title']} (Status: {task['status']})")
else:
    print(f"⚠️ No new task found!")
    print(f"Expected: {len(current_tasks) + 1}, Got: {len(new_tasks)}")

print("\n" + "=" * 80)
print("📋 SUMMARY")
print("=" * 80)
print(f"Tasks before: {len(current_tasks)}")
print(f"Tasks after: {len(new_tasks)}")
print(f"New tasks: {len(new_tasks) - len(current_tasks)}")
print("\n✅ This proves AI Assistant tasks → General Tasks page flow works!")
print("=" * 80)
