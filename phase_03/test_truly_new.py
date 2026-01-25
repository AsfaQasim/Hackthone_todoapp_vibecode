import requests
import json

# Create a completely new user
signup_url = "http://localhost:8000/api/signup"
signup_payload = {
    "email": "trulynewuser@example.com",
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
        
        # Immediately try to use this token
        # Now test the tasks endpoint with the token
        tasks_url = "http://localhost:8000/api/tasks"
        auth_headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        
        tasks_response = requests.get(tasks_url, headers=auth_headers)
        print(f"Tasks GET Status: {tasks_response.status_code}")
        print(f"Tasks GET Response: {tasks_response.text}")
        
        if tasks_response.status_code == 200:
            print("SUCCESS: Authentication is working!")
        else:
            print("FAILURE: Authentication still not working")
        
except Exception as e:
    print(f"Error: {e}")