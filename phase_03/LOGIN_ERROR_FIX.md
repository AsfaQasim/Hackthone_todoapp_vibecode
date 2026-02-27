# Login Error Fix - "Login failed due to an internal server error"

## Error Message
```
Login API error: Login failed due to an internal server error
Login function returned: false
```

## Root Causes

### 1. Backend Not Running
The most common cause - backend server is not started.

### 2. Database Connection Failed
Backend can't connect to PostgreSQL database.

### 3. Environment Variables Missing
Required secrets not configured.

### 4. Port Conflict
Backend port 8000 already in use.

## Quick Fix - Step by Step

### Step 1: Check if Backend is Running

**Test:**
```bash
curl http://localhost:8000/health
```

**Expected Response:**
```json
{"status":"healthy","service":"AI Chatbot with MCP"}
```

**If Error:** Backend is not running → Go to Step 2

### Step 2: Start Backend

```bash
cd backend
python main.py
```

**Expected Output:**
```
INFO:     Started server process
INFO:     Waiting for application startup.
Starting AI Chatbot MCP...
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Step 3: Check Environment Variables

**File:** `backend/.env`

**Required Variables:**
```env
DATABASE_URL=postgresql://user:pass@host/db
BETTER_AUTH_SECRET=your_secret_key_here
JWT_SECRET=your_jwt_secret_here
OPENAI_API_KEY=sk-...
```

**Check:**
```bash
cd backend
type .env
```

### Step 4: Test Database Connection

```bash
cd backend
python -c "from src.db import init_db; init_db(); print('✅ Database connected!')"
```

### Step 5: Test Login Endpoint Directly

```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"test123\"}"
```

**Expected Response:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user_id": "..."
}
```

### Step 6: Check Backend Logs

Look for errors in the terminal where backend is running:

**Common Errors:**

1. **Database Connection Error:**
```
sqlalchemy.exc.OperationalError: could not connect to server
```
**Fix:** Check DATABASE_URL in .env

2. **Missing Secret:**
```
KeyError: 'BETTER_AUTH_SECRET'
```
**Fix:** Add BETTER_AUTH_SECRET to .env

3. **Port Already in Use:**
```
OSError: [Errno 48] Address already in use
```
**Fix:** Kill process on port 8000

## Detailed Troubleshooting

### Issue 1: Backend Won't Start

**Symptoms:**
- `python main.py` shows errors
- Import errors
- Module not found

**Solutions:**

**A. Install Dependencies:**
```bash
cd backend
pip install -r requirements.txt
```

**B. Check Python Version:**
```bash
python --version
# Should be Python 3.8+
```

**C. Activate Virtual Environment (if using):**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### Issue 2: Database Connection Failed

**Symptoms:**
- Backend starts but login fails
- "OperationalError" in logs
- "could not connect to server"

**Solutions:**

**A. Check Database URL:**
```bash
# In backend/.env
DATABASE_URL=postgresql://neondb_owner:password@host/neondb?sslmode=require
```

**B. Test Connection:**
```bash
cd backend
python
>>> from src.db import engine
>>> engine.connect()
# Should not throw error
```

**C. Check Database is Running:**
- For Neon: Check dashboard
- For local PostgreSQL: `pg_isready`

### Issue 3: CORS Error

**Symptoms:**
- Frontend shows "Failed to fetch"
- Browser console shows CORS error

**Solution:**

Check `backend/main.py` has correct CORS settings:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue 4: Port 8000 Already in Use

**Symptoms:**
- "Address already in use"
- Backend won't start

**Solutions:**

**Windows:**
```cmd
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Linux/Mac:**
```bash
lsof -ti:8000 | xargs kill -9
```

**Or use different port:**
```bash
uvicorn main:app --port 8001
```

Then update frontend `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8001
```

## Testing Login Flow

### Test 1: Backend Health
```bash
curl http://localhost:8000/health
```

### Test 2: Login Endpoint
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test"}'
```

### Test 3: Frontend API Proxy
```bash
curl -X POST http://localhost:3000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"test"}'
```

### Test 4: Full Login Flow
1. Open http://localhost:3000/login
2. Open browser console (F12)
3. Enter email and password
4. Click "Sign in"
5. Check console for logs

**Expected Console Output:**
```
Calling login function...
Login API result: {data: {...}, error: null}
Login successful, GuestOnlyRoute will handle redirect...
```

## Environment Setup Checklist

### Backend (.env)
- [ ] DATABASE_URL set
- [ ] BETTER_AUTH_SECRET set
- [ ] JWT_SECRET set
- [ ] OPENAI_API_KEY set (if using AI features)

### Frontend (.env.local)
- [ ] NEXT_PUBLIC_API_URL=http://localhost:8000
- [ ] BETTER_AUTH_SECRET (same as backend)
- [ ] JWT_SECRET (same as backend)

## Complete Reset (Nuclear Option)

If nothing works, try complete reset:

```bash
# 1. Stop everything
taskkill /F /IM node.exe
taskkill /F /IM python.exe

# 2. Backend
cd backend
pip install -r requirements.txt
python main.py

# 3. Frontend (new terminal)
cd frontend
rmdir /s /q .next
npm install
npm run dev

# 4. Test
curl http://localhost:8000/health
curl http://localhost:3000
```

## Common Error Messages & Fixes

| Error | Cause | Fix |
|-------|-------|-----|
| "Failed to fetch" | Backend not running | Start backend |
| "CORS error" | CORS not configured | Check CORS settings |
| "Unauthorized" | Token invalid | Check JWT_SECRET matches |
| "Internal server error" | Database issue | Check DATABASE_URL |
| "Connection refused" | Wrong port | Check NEXT_PUBLIC_API_URL |

## Success Indicators

✅ Backend running on port 8000
✅ Frontend running on port 3000
✅ `/health` endpoint returns 200
✅ `/login` endpoint returns token
✅ Browser console shows no errors
✅ Login redirects to dashboard

## Still Not Working?

### Check These:

1. **Backend Terminal:**
   - Any error messages?
   - Is it listening on 8000?

2. **Frontend Terminal:**
   - Any build errors?
   - Is it on port 3000?

3. **Browser Console (F12):**
   - Network tab - check /api/login request
   - Console tab - check for errors
   - Application tab - check cookies

4. **Database:**
   - Can you connect manually?
   - Does `user` table exist?

### Get Help:

Share these details:
1. Backend terminal output
2. Frontend terminal output
3. Browser console errors
4. Network tab screenshot

Your login will work after following these steps! 🚀
