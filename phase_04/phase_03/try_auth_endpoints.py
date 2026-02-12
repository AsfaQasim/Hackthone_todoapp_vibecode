import requests
import json

# Try to create a user via the signup endpoint
signup_data = {
    "email": "testuser@example.com",
    "password": "securepassword123"
}

try:
    response = requests.post('http://localhost:8000/api/auth/register', json=signup_data)
    print("Signup response:", response.status_code)
    print("Response:", response.text)
except Exception as e:
    print("Signup request failed:", str(e))

# If signup isn't available, try login
try:
    login_data = {
        "email": "testuser@example.com",
        "password": "securepassword123"
    }
    response = requests.post('http://localhost:8000/api/auth/login', json=login_data)
    print("Login response:", response.status_code)
    print("Response:", response.text)
except Exception as e:
    print("Login request failed:", str(e))