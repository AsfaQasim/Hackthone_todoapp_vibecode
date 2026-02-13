"""Create test tasks via API."""
import requests

print("Creating test tasks...")
print("=" * 70)

# First, login to get token
print("\n1. Logging in...")
response = requests.post(
    "http://localhost:8000/login",
    json={"email": "asfaqasim145@gmail.com", "password": "test123"}
)

if response.status_code == 200:
    data = response.json()
    token = data.get('token') or data.get('access_token')
    print(f"✅ Token received: {token[:30]}...")
    
    # Create test tasks
    test_tasks = [
        {"title": "Complete project documentation", "description": "Write comprehensive docs"},
        {"title": "Review pull requests", "description": "Check team's code submissions"},
        {"title": "Update dependencies", "description": "Upgrade npm packages"},
        {"title": "Fix bug in login flow", "description": "Resolve authentication issue"},
        {"title": "Prepare presentation", "description": "Create slides for meeting"}
    ]
    
    print(f"\n2. Creating {len(test_tasks)} test tasks...")
    
    for i, task_data in enumerate(test_tasks, 1):
        response = requests.post(
            "http://localhost:8000/api/tasks",
            headers={"Authorization": f"Bearer {token}"},
            json=task_data
        )
        
        if response.status_code == 200:
            task = response.json()
            print(f"  ✅ Task {i}: {task['title']}")
        else:
            print(f"  ❌ Task {i} failed: {response.status_code} - {response.text}")
    
    # Verify
    print("\n3. Verifying tasks...")
    response = requests.get(
        "http://localhost:8000/api/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    if response.status_code == 200:
        tasks = response.json()
        print(f"✅ Total tasks now: {len(tasks)}")
        for task in tasks:
            print(f"  - {task['title']} ({task['status']})")
    else:
        print(f"❌ Failed to fetch tasks: {response.status_code}")
        
else:
    print(f"❌ Login failed: {response.status_code}")

print("\n" + "=" * 70)
print("\n✅ Now go to: http://localhost:3000/general-task-execution")
print("   You should see your tasks!")
