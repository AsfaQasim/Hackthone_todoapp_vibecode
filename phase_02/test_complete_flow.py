import requests
import json

# Create a new user first
signup_url = "http://localhost:8000/api/signup"
signup_payload = {
    "email": "testuser123@example.com",
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
            "title": "Test task from verification",
            "description": "This is a test task to verify the flow"
        }

        create_response = requests.post(create_task_url, data=json.dumps(task_payload), headers=auth_headers)
        print(f"Task Creation Status: {create_response.status_code}")
        print(f"Task Creation Response: {create_response.text}")

        # Get the created task to verify
        if create_response.status_code == 200:
            created_task = create_response.json()
            task_id = created_task.get('id')
            if task_id:
                get_task_url = f"http://localhost:8000/api/tasks/{task_id}"
                get_task_response = requests.get(get_task_url, headers=auth_headers)
                print(f"Get Task Status: {get_task_response.status_code}")
                print(f"Get Task Response: {get_task_response.text}")

                # Test updating the task
                update_task_url = f"http://localhost:8000/api/tasks/{task_id}"
                update_payload = {
                    "title": "Updated test task",
                    "description": "This task has been updated"
                }
                update_response = requests.put(update_task_url, data=json.dumps(update_payload), headers=auth_headers)
                print(f"Update Task Status: {update_response.status_code}")
                print(f"Update Task Response: {update_response.text}")

                # Test toggling completion
                toggle_complete_url = f"http://localhost:8000/api/tasks/{task_id}/complete"
                toggle_response = requests.patch(toggle_complete_url, headers=auth_headers)
                print(f"Toggle Completion Status: {toggle_response.status_code}")
                print(f"Toggle Completion Response: {toggle_response.text}")

                # Clean up - delete the task
                delete_response = requests.delete(get_task_url, headers=auth_headers)
                print(f"Delete Task Status: {delete_response.status_code}")
                print(f"Delete Task Response: {delete_response.text}")

except Exception as e:
    print(f"Error: {e}")