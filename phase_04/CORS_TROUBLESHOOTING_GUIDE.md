# CORS Error Troubleshooting Guide

## Understanding the Issue

CORS (Cross-Origin Resource Sharing) error browser mein tab aata hai jab:
1. Frontend (localhost:3000) directly Backend (localhost:8000) ko call karta hai
2. Backend mein proper CORS headers configured nahi hain
3. Ya koi network/connection issue hai

## Our Architecture

```
Browser (localhost:3000)
    ↓
Next.js Frontend
    ↓
Next.js API Route (/api/tasks) [Server-side, NO CORS needed]
    ↓
FastAPI Backend (localhost:8000) [CORS configured]
```

## Quick Fix Steps

### Step 1: Run Diagnosis
```bash
python diagnose_cors_issue.py
```

### Step 2: Check Backend is Running
```bash
# Backend should be running on http://localhost:8000
# Test with:
curl http://localhost:8000/health
```

### Step 3: Check Frontend is Running
```bash
# Frontend should be running on http://localhost:3000
# Test with:
curl http://localhost:3000/api/health
```

### Step 4: Restart Everything
```bash
COMPLETE_CORS_FIX.bat
```

## Common Issues & Solutions

### Issue 1: "Failed to fetch" in Browser Console

**Cause:** Backend not running or wrong URL

**Solution:**
```bash
cd backend
python main.py
```

### Issue 2: CORS Error Despite Using Next.js API Route

**Cause:** Frontend code accidentally calling backend directly

**Check:** Open browser DevTools → Network tab
- ✅ Good: Request to `/api/tasks` (relative URL)
- ❌ Bad: Request to `http://localhost:8000/api/tasks` (absolute URL)

**Solution:** Make sure frontend uses relative URLs:
```typescript
// ✅ Correct
fetch('/api/tasks', { ... })

// ❌ Wrong
fetch('http://localhost:8000/api/tasks', { ... })
```

### Issue 3: Backend Returns 401 Unauthorized

**Cause:** Token not being sent or invalid

**Solution:**
1. Check if auth_token cookie exists
2. Check if Authorization header is being sent
3. Verify token is valid

### Issue 4: Backend Returns Empty Array

**Cause:** No tasks in database for user

**Solution:** This is normal! Use AI assistant to create tasks:
1. Go to http://localhost:3000/chat
2. Type: "add task: Buy groceries"
3. Check http://localhost:3000/general-task-execution

## Debugging Steps

### 1. Check Browser Console
```
F12 → Console tab
Look for:
- "Failed to fetch"
- "CORS error"
- "Network error"
```

### 2. Check Network Tab
```
F12 → Network tab
Look for:
- Failed requests (red)
- Request URL (should be /api/tasks, not localhost:8000)
- Response status (200, 401, 500, etc.)
```

### 3. Check Backend Logs
```
Backend terminal should show:
- "Starting AI Chatbot MCP..."
- "🔧 CORS allowed origins: ['http://localhost:3000', ...]"
- Request logs when you try to fetch tasks
```

### 4. Check Frontend Logs
```
Frontend terminal should show:
- "ready - started server on 0.0.0.0:3000"
- No compilation errors
```

## Testing CORS Manually

### Test 1: Backend Health
```bash
curl http://localhost:8000/health
```
Expected: `{"status":"healthy","service":"AI Chatbot with MCP"}`

### Test 2: Backend CORS Headers
```bash
curl -X OPTIONS http://localhost:8000/api/tasks \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: GET" \
  -v
```
Expected: Response should include `access-control-allow-origin: http://localhost:3000`

### Test 3: Frontend API Proxy
```bash
curl http://localhost:3000/api/health
```
Expected: Should return backend health status

## Still Having Issues?

1. **Clear browser cache:**
   - Chrome: Ctrl+Shift+Delete → Clear cache
   - Or use Incognito mode

2. **Check .env files:**
   ```bash
   # backend/.env
   ALLOWED_ORIGINS=http://localhost:3000,https://*.vercel.app
   
   # frontend/.env.local
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

3. **Restart everything fresh:**
   ```bash
   # Kill all processes
   taskkill /F /IM node.exe
   taskkill /F /IM python.exe
   
   # Start backend
   cd backend
   python main.py
   
   # Start frontend (new terminal)
   cd frontend
   npm run dev
   ```

4. **Check if ports are already in use:**
   ```bash
   # Check port 8000
   netstat -ano | findstr :8000
   
   # Check port 3000
   netstat -ano | findstr :3000
   ```

## Success Indicators

✅ Backend running: `http://localhost:8000/health` returns 200
✅ Frontend running: `http://localhost:3000` loads
✅ No CORS errors in browser console
✅ Network tab shows requests to `/api/tasks` (not `localhost:8000`)
✅ Tasks load successfully (even if empty array)

## Contact Points

If issue persists:
1. Share browser console screenshot
2. Share network tab screenshot
3. Share backend terminal logs
4. Share frontend terminal logs
