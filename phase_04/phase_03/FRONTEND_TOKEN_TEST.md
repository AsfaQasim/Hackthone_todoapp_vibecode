# Test with Frontend Token

## Step 1: Get Your Frontend Token

1. Open your browser
2. Go to general-task-execution page
3. Press F12 (Developer Tools)
4. Go to Console tab
5. Run this command:

```javascript
document.cookie.split('; ').find(row => row.startsWith('auth_token='))
```

6. Copy the token value (everything after `auth_token=`)

## Step 2: Test with Your Token

Replace `YOUR_TOKEN_HERE` with your actual token and run:

```python
import requests
import json
import base64

token = "YOUR_TOKEN_HERE"  # Paste your token here

# Decode to get user ID
payload = token.split('.')[1] + '=' * (4 - len(token.split('.')[1]) % 4)
user_data = json.loads(base64.b64decode(payload))
user_id = user_data.get('sub') or user_data.get('userId') or user_data.get('user_id')

print(f"User ID: {user_id}")
print(f"Email: {user_data.get('email')}")

# Test API
response = requests.get(
    f"http://localhost:8000/api/{user_id}/tasks",
    headers={"Authorization": f"Bearer {token}"}
)

print(f"\nStatus: {response.status_code}")
if response.status_code == 200:
    tasks = response.json()
    print(f"Tasks: {len(tasks)}")
    for task in tasks:
        print(f"  - {task['title']}")
else:
    print(f"Error: {response.text}")
```

## OR Simpler Way

Just run this in browser console on general-task-execution page:

```javascript
// Get token
const cookies = document.cookie.split('; ');
const authToken = cookies.find(row => row.startsWith('auth_token='));
const token = authToken ? authToken.split('=')[1] : null;

// Decode to get user ID
const payload = JSON.parse(atob(token.split('.')[1]));
const userId = payload.sub || payload.userId || payload.user_id;

console.log('User ID:', userId);
console.log('Email:', payload.email);

// Test backend API directly
fetch(`http://localhost:8000/api/${userId}/tasks`, {
  headers: {
    'Authorization': `Bearer ${token}`
  }
})
.then(r => r.json())
.then(data => {
  console.log('Backend tasks:', data.length);
  console.log(data);
})
.catch(err => console.error('Error:', err));
```

This will show if backend has tasks for YOUR frontend user!
