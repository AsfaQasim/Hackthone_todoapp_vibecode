# Complete Fix for Task Display Issue

## Problem
- Tasks create ho rahe hain but general-task-execution page pe show nahi ho rahe
- Backend API se tasks mil rahe hain (13 tasks)
- Frontend ko empty array mil raha hai

## Root Cause
Frontend aur backend different users use kar rahe hain because:
1. Backend database mein user save nahi ho raha (memory mode)
2. Frontend ka user alag hai test script ke user se

## Solution Steps

### Step 1: Backend Restart (MUST DO)
```bash
# Backend terminal mein
cd backend
python main.py
```

### Step 2: Frontend Restart (MUST DO)
```bash
# Frontend terminal mein
# Ctrl+C to stop
npm run dev
```

### Step 3: Fresh Start
1. Browser mein logout karo
2. Fresh login karo with: asfaqasim145@gmail.com
3. Chat page pe jao
4. Message bhejo: "hello" (yeh user ko backend mein create karega)
5. Phir message bhejo: "Add task: eating"
6. Response check karo - "✅ I've added..." dikhna chahiye

### Step 4: Verify
1. General-task-execution page pe jao
2. Tasks dikhne chahiye

## If Still Not Working

Run this in browser console on general-task-execution page:

```javascript
// Step 1: Get token and user info
const cookies = document.cookie.split('; ');
const authToken = cookies.find(row => row.startsWith('auth_token='));
const token = authToken ? authToken.split('=')[1] : null;
const payload = JSON.parse(atob(token.split('.')[1]));
const userId = payload.sub || payload.userId || payload.user_id;

console.log('=== DEBUG INFO ===');
console.log('User ID:', userId);
console.log('Email:', payload.email);

// Step 2: Test frontend API
fetch('/api/tasks', {
  headers: { 'Authorization': `Bearer ${token}` }
})
.then(r => r.json())
.then(data => console.log('Frontend API tasks:', data));

// Step 3: Test backend API directly
fetch(`http://localhost:8000/api/${userId}/tasks`, {
  headers: { 'Authorization': `Bearer ${token}` }
})
.then(r => r.json())
.then(data => console.log('Backend API tasks:', data));
```

## Expected Output
```
Frontend API tasks: [array of tasks]
Backend API tasks: [same array of tasks]
```

If frontend shows [] but backend shows tasks, then frontend /api/tasks route has issue.

## Last Resort - Manual Database Fix

If nothing works, run this Python script:

```python
import sqlite3
import uuid

# Your email
email = "asfaqasim145@gmail.com"

# Connect to backend database
conn = sqlite3.connect("backend/todo_app_local.db")
cursor = conn.cursor()

# Create user manually
user_id = str(uuid.uuid4())
cursor.execute(
    "INSERT INTO users (id, email, name, created_at, updated_at) VALUES (?, ?, ?, datetime('now'), datetime('now'))",
    (user_id, email, email.split('@')[0])
)

# Create a test task
task_id = str(uuid.uuid4())
cursor.execute(
    "INSERT INTO tasks (id, user_id, title, description, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, datetime('now'), datetime('now'))",
    (task_id, user_id, "Test Task", "Manual test", "pending")
)

conn.commit()
conn.close()

print(f"User created: {email}")
print(f"User ID: {user_id}")
print("Now login with this email and check!")
```

## Contact Me
Tell me:
1. Did you restart both backend and frontend?
2. What does browser console show after running the JavaScript code?
3. Are backend and frontend both running on correct ports (8000 and 3000)?
