import requests
import json

# Test the login endpoint with an existing user first
login_url = "http://localhost:8000/api/login"

login_payload = {
    "email": "testuser@example.com",  # From our earlier successful signup
    "password": "password123"
}

headers = {
    "Content-Type": "application/json"
}

try:
    # First, login to get a token
    login_response = requests.post(login_url, data=json.dumps(login_payload), headers=headers)
    print(f"Login Status Code: {login_response.status_code}")
    
    if login_response.status_code == 200:
        login_data = login_response.json()
        token = login_data.get('access_token')
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
    else:
        print(f"Login failed: {login_response.text}")
        
        # Try signing up a new user instead
        signup_url = "http://localhost:8000/api/signup"
        signup_payload = {
            "email": "newtestuser@example.com",
            "password": "password123"
        }
        
        signup_response = requests.post(signup_url, data=json.dumps(signup_payload), headers=headers)
        print(f"New Signup Status Code: {signup_response.status_code}")
        print(f"New Signup Response: {signup_response.text}")
        
        if signup_response.status_code == 200:
            signup_data = signup_response.json()
            token = signup_data.get('access_token')
            print(f"Received token from signup: {token[:20]}..." if token else "No token received")
            
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