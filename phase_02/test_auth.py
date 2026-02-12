import requests
import json

# Test the login endpoint
url = "http://localhost:8000/api/login"

payload = {
    "email": "asfaqasim144@gmail.com",
    "password": "password123"
}

headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(f"Login Status Code: {response.status_code}")
    print(f"Login Response: {response.text}")
except Exception as e:
    print(f"Login Error: {e}")

# Also test the signup again to make sure it still works
url = "http://localhost:8000/api/signup"

payload = {
    "email": "testuser@example.com",
    "password": "password123"
}

try:
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(f"Signup Status Code: {response.status_code}")
    print(f"Signup Response: {response.text}")
except Exception as e:
    print(f"Signup Error: {e}")