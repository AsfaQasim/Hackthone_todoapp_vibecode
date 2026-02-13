# Diagnosing "Failed to fetch" Error for AI Tasks

## What I've Done

I've updated the AI Tasks page (`frontend/app/general-task-execution/page.tsx`) with better error logging and diagnostics.

## Steps to Fix

### 1. Check if Backend is Running

Open a terminal and run:
```bash
curl http://localhost:8000/health
```

You should see: `{"status":"healthy","service":"AI Chatbot with MCP"}`

If not, start the backend:
```bash
cd backend
python main.py
```

### 2. Check Browser Console

1. Open the AI Tasks page in your browser
2. Press F12 to open Developer Tools
3. Go to the "Console" tab
4. Look for these log messages:

```
=== loadTasks called ===
Auth token found: true/false
Token format check: Valid JWT format / Invalid JWT format
Fetching from: http://localhost:8000/api/tasks
Token being sent: eyJhbGciOiJIUzI1NiIs...
API response status: 200/401/500
```

### 3. Common Issues and Solutions

#### Issue: "Auth token found: false"
**Solution:** You're not logged in. Go to `/login` and log in again.

#### Issue: "Invalid JWT format"
**Solution:** Your token is corrupted. Clear cookies and log in again:
- Press F12 → Application tab → Cookies → Delete `auth_token`
- Log in again

#### Issue: "Cannot connect to backend server"
**Solution:** Backend is not running on port 8000
- Start backend: `cd backend && python main.py`
- Check if port 8000 is available

#### Issue: "API response status: 401"
**Solution:** Token is expired or invalid
- Log out and log in again
- Check backend logs for token validation errors

#### Issue: "API response status: 500"
**Solution:** Backend error
- Check backend terminal for error messages
- Check backend logs: `backend/app.log`

#### Issue: "Network error: Cannot reach backend server"
**Solution:** CORS or network issue
- Make sure backend CORS is configured (it should be)
- Check if firewall is blocking port 8000
- Try accessing http://localhost:8000/health directly in browser

### 4. Test the Endpoint Directly

Create a test file `test_ai_tasks_endpoint.py`:

```python
import requests

# Get your token from browser cookies (F12 → Application → Cookies → auth_token)
TOKEN = "paste_your_token_here"

response = requests.get(
    "http://localhost:8000/api/tasks",
    headers={"Authorization": f"Bearer {TOKEN}"}
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text}")
```

Run it:
```bash
python test_ai_tasks_endpoint.py
```

### 5. Check Backend Logs

Look at the backend terminal or `backend/app.log` for errors when you try to load tasks.

## What to Tell Me

After checking the above, please share:

1. Backend health check result
2. Browser console logs (the ones I mentioned above)
3. Backend terminal output when you load the AI Tasks page
4. Your token (first 20 characters only): `eyJhbGciOiJIUzI1NiIs...`

This will help me identify the exact issue!
