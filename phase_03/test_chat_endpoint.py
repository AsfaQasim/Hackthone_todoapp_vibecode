import requests
import json

# Test the chat endpoint with a dummy token to see what error occurs
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer dummy_token'
}

data = {
    'message': 'Hello',
    'conversation_id': None
}

try:
    response = requests.post('http://localhost:8000/api/user123/chat', headers=headers, json=data)
    print("Chat endpoint response:", response.status_code)
    print("Response text:", response.text[:500])  # First 500 chars
    try:
        print("Response JSON:", response.json())
    except:
        print("Response is not valid JSON")
except Exception as e:
    print("Chat endpoint request failed:", str(e))