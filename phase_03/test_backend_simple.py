import requests
import json

# Test the backend health endpoint
try:
    response = requests.get('http://localhost:8000/health')
    print("Health check:", response.status_code, response.json())
except Exception as e:
    print("Health check failed:", str(e))

# Test the root endpoint
try:
    response = requests.get('http://localhost:8000/')
    print("Root endpoint:", response.status_code, response.json())
except Exception as e:
    print("Root endpoint failed:", str(e))