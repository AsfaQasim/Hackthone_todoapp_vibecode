import requests

# Login first
login_data = {
    "email": "asfaqasim145@gmail.com",
    "password": "test123"
}

print("1. Logging in...")
login_response = requests.post("http://localhost:8000/login", json=login_data)
print(f"Login status: {login_response.status_code}")

if login_response.status_code == 200:
    login_result = login_response.json()
    token = login_result.get('access_token')
    user_id = login_result.get('user_id')
    
    print(f"User ID: {user_id}")
    print(f"Token: {token[:20]}...")
    
    # Test tasks endpoint
    print("\n2. Fetching tasks...")
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    tasks_url = f"http://localhost:8000/api/{user_id}/tasks"
    print(f"URL: {tasks_url}")
    
    tasks_response = requests.get(tasks_url, headers=headers)
    print(f"Tasks status: {tasks_response.status_code}")
    
    if tasks_response.status_code == 200:
        tasks = tasks_response.json()
        print(f"✅ Found {len(tasks)} tasks:")
        for task in tasks:
            print(f"  - {task.get('title')} (status: {task.get('status')})")
    else:
        print(f"❌ Error: {tasks_response.text}")
else:
    print(f"❌ Login failed: {login_response.text}")
