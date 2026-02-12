import requests
import json

# First, let's try to login with the user we just created
login_url = "http://localhost:8000/api/login"
login_payload = {
    "email": "finalworkingtest@example.com",
    "password": "password123"
}

headers = {
    "Content-Type": "application/json"
}

try:
    # Login to get a token
    login_response = requests.post(login_url, data=json.dumps(login_payload), headers=headers)
    print(f"Login Status Code: {login_response.status_code}")
    print(f"Login Response: {login_response.text}")
    
    if login_response.status_code == 200:
        login_data = login_response.json()
        token = login_data.get('access_token')
        print(f"Received token from login: {token[:20]}..." if token else "No token received")
        
        # Now test the tasks endpoint with the token from login
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
            "title": "Test task from login token",
            "description": "This is a test task using login token"
        }
        
        create_response = requests.post(create_task_url, data=json.dumps(task_payload), headers=auth_headers)
        print(f"Task Creation Status: {create_response.status_code}")
        print(f"Task Creation Response: {create_response.text}")
        
except Exception as e:
    print(f"Error: {e}")