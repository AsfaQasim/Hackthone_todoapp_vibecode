
import requests
import json

# Test the signup endpoint
url = "http://localhost:8000/api/signup"

payload = {
    "email": "asfaqasim144@gmail.com",
    "password": "password123"
}

headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")