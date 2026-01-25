import requests
import json

# Test the updated signup endpoint with a new email
url = "http://localhost:8000/api/signup"

payload = {
    "email": "testuser3@example.com",
    "password": "password123"
}

headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(f"Signup Status Code: {response.status_code}")
    print(f"Signup Response: {response.text}")
    
    # Extract the token from the response
    if response.status_code == 200:
        data = response.json()
        token = data.get('access_token')
        print(f"Received token: {token[:20]}..." if token else "No token received")
        
        # Now test the tasks endpoint with the token
        tasks_url = "http://localhost:8000/api/tasks"
        auth_headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        tasks_response = requests.get(tasks_url, headers=auth_headers)
        print(f"Tasks GET Status: {tasks_response.status_code}")
        print(f"Tasks GET Response: {tasks_response.text}")
        
        # Test creating a task
        create_task_url = "http://localhost:8000/api/tasks"
        task_payload = {
            "title": "Test task from API",
            "description": "This is a test task"
        }
        
        create_response = requests.post(create_task_url, data=json.dumps(task_payload), headers=auth_headers)
        print(f"Task Creation Status: {create_response.status_code}")
        print(f"Task Creation Response: {create_response.text}")
        
except Exception as e:
    print(f"Error: {e}")