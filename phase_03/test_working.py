import requests
import json

# Create a new user first
signup_url = "http://localhost:8000/api/signup"
signup_payload = {
    "email": "workingtestuser@example.com",
    "password": "password123"
}

headers = {
    "Content-Type": "application/json"
}

try:
    # Sign up a new user
    signup_response = requests.post(signup_url, data=json.dumps(signup_payload), headers=headers)
    print(f"Signup Status Code: {signup_response.status_code}")
    print(f"Signup Response: {signup_response.text}")
    
    if signup_response.status_code == 200:
        signup_data = signup_response.json()
        token = signup_data.get('access_token')
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
            "title": "Working test task",
            "description": "This should work now"
        }
        
        create_response = requests.post(create_task_url, data=json.dumps(task_payload), headers=auth_headers)
        print(f"Task Creation Status: {create_response.status_code}")
        print(f"Task Creation Response: {create_response.text}")
        
        # If successful, also test updating and deleting
        if create_response.status_code == 200:
            task_data = create_response.json()
            task_id = task_data.get('id')
            if task_id:
                # Update the task
                update_url = f"http://localhost:8000/api/tasks/{task_id}"
                update_payload = {
                    "title": "Updated working test task",
                    "description": "This task has been updated"
                }
                
                update_response = requests.put(update_url, data=json.dumps(update_payload), headers=auth_headers)
                print(f"Task Update Status: {update_response.status_code}")
                print(f"Task Update Response: {update_response.text}")
                
                # Delete the task
                delete_response = requests.delete(update_url, headers=auth_headers)
                print(f"Task Delete Status: {delete_response.status_code}")
                print(f"Task Delete Response: {delete_response.text}")
        
except Exception as e:
    print(f"Error: {e}")