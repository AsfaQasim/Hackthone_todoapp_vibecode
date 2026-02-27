# Debug Login Failure - Step by Step

## Error Message
```
❌ [LoginPage] Login failed
```

## What to Check

### Step 1: Open Browser Console (F12)

Look for these logs in order:

#### Expected Success Flow:
```
🔐 [LoginPage] Calling login function...
📧 [LoginPage] Email: test@example.com
🔐 [AuthContext] Attempting login with email: test@example.com
🔐 [auth-client] Calling /api/login
📡 [/api/login] Forwarding to backend
📥 [/api/login] Backend response status: 200
✅ [auth-client] Login successful
✅ [AuthContext] Token saved to cookies
✅ [LoginPage] Login successful!
```

#### What You're Seeing (Failure):
```
🔐 [LoginPage] Calling login function...
❌ [LoginPage] Login failed
```

### Step 2: Find the Actual Error

Scroll up in console to find one of these errors:

#### Error 1: Backend Not Running
```
❌ [/api/login] Login proxy error: fetch failed
❌ [auth-client] Sign in error: Network error
```

**Solution:**
```bash
cd backend
python main.py
```

#### Error 2: Backend Returns Error
```
📥 [/api/login] Backend response status: 500
❌ [auth-client] Login failed: Login failed due to internal server error
```

**Solution:** Check backend terminal for errors

#### Error 3: No Token in Response
```
❌ [AuthContext] No access_token in login response
```

**Solution:** Backend not returning token properly

#### Error 4: Token Decode Failed
```
❌ [AuthContext] Could not decode token after login
```

**Solution:** Token format is wrong

### Step 3: Check Backend

**Test backend directly:**
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@test.com\",\"password\":\"test\"}"
```

**Expected Response:**
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user_id": "..."
}
```

**If Error:**
- Backend not running → Start it
- Database error → Check DATABASE_URL
- Missing secret → Check BETTER_AUTH_SECRET

### Step 4: Check Network Tab

1. Open browser DevTools (F12)
2. Go to "Network" tab
3. Try login again
4. Look for `/api/login` request

**Click on it and check:**

**Request:**
- Method: POST
- URL: http://localhost:3000/api/login
- Body: {"email":"...","password":"..."}

**Response:**
- Status: Should be 200
- Body: Should have access_token

**Common Issues:**

| Status | Meaning | Solution |
|--------|---------|----------|
| 500 | Backend error | Check backend logs |
| 404 | Route not found | Check API route exists |
| 0 | Network error | Backend not running |
| 401 | Unauthorized | Wrong credentials |

### Step 5: Check Backend Logs

Look at terminal where backend is running:

**Success:**
```
🔐 LOGIN REQUEST: test@test.com
✅ Existing user found: test@test.com
🔑 Final user_id being returned: ...
```

**Failure:**
```
❌ Login error: ...
❌ Database connection failed
❌ Missing environment variable
```

## Common Issues & Solutions

### Issue 1: Backend Not Running

**Symptoms:**
```
❌ [/api/login] Login proxy error: fetch failed
Failed to fetch
```

**Solution:**
```bash
cd backend
python main.py
```

**Verify:**
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

### Issue 2: Database Connection Error

**Symptoms:**
```
Backend logs show:
sqlalchemy.exc.OperationalError: could not connect
```

**Solution:**

Check `backend/.env`:
```env
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
```

**Test connection:**
```bash
cd backend
python -c "from src.db import engine; engine.connect(); print('✅ Connected!')"
```

### Issue 3: Missing Environment Variables

**Symptoms:**
```
KeyError: 'BETTER_AUTH_SECRET'
```

**Solution:**

Create/update `backend/.env`:
```env
BETTER_AUTH_SECRET=your_secret_key_here_at_least_32_chars
JWT_SECRET=your_jwt_secret_here
DATABASE_URL=postgresql://...
```

**Verify:**
```bash
cd backend
type .env
```

### Issue 4: CORS Error

**Symptoms:**
```
Access to fetch at 'http://localhost:8000/login' from origin 'http://localhost:3000' has been blocked by CORS
```

**Solution:**

Check `backend/main.py` has:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue 5: Port Already in Use

**Symptoms:**
```
OSError: [Errno 48] Address already in use
```

**Solution:**

**Windows:**
```cmd
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Then restart:**
```bash
cd backend
python main.py
```

## Quick Diagnostic Commands

### 1. Check Backend Health
```bash
curl http://localhost:8000/health
```

### 2. Test Login Endpoint
```bash
curl -X POST http://localhost:8000/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@test.com\",\"password\":\"test\"}"
```

### 3. Check Frontend API
```bash
curl -X POST http://localhost:3000/api/login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@test.com\",\"password\":\"test\"}"
```

### 4. Check Environment Variables
```bash
cd backend
type .env | findstr DATABASE_URL
type .env | findstr BETTER_AUTH_SECRET
```

## Complete Reset (If Nothing Works)

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
```

## What to Share for Help

If still not working, share:

1. **Full console output** (all logs from browser console)
2. **Backend terminal output** (what backend shows)
3. **Network tab screenshot** (showing /api/login request)
4. **Backend .env file** (hide sensitive values)

Example:
```
Console shows:
❌ [/api/login] Login proxy error: fetch failed

Backend terminal shows:
INFO:     Uvicorn running on http://127.0.0.1:8000

Network tab shows:
POST /api/login - Status: (failed) net::ERR_CONNECTION_REFUSED
```

## Most Likely Issue

Based on the error, **backend is probably not running**.

**Quick Fix:**
```bash
# Terminal 1
cd backend
python main.py

# Terminal 2
cd frontend
npm run dev

# Browser
http://localhost:3000/login
```

Try login again! 🚀
