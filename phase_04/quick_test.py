import requests
import json
import base64

# Register
r = requests.post("http://localhost:8000/register", json={"email": "quicktest@test.com", "password": "test"})
token = r.json()['access_token']
payload = token.split('.')[1] + '=' * (4 - len(token.split('.')[1]) % 4)
user_id = json.loads(base64.b64decode(payload)).get('sub')

print(f"User: {user_id}")
print(f"Token: {token[:20]}...")

# Test chat
r = requests.post(
    f"http://localhost:8000/api/{user_id}/chat",
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    json={"message": "Add task: Test simple chat"}
)

print(f"\nStatus: {r.status_code}")
print(json.dumps(r.json(), indent=2))
