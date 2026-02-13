# CORS Fix - Step by Step

## Problem
All requests are blocked with "Missing Access-Control-Allow-Origin header"

## Root Cause
Backend is either:
1. Not running
2. Running but not accessible
3. CORS middleware not properly configured

## Solution

### Step 1: Restart Backend with CORS
```bash
FIX_CORS_COMPLETE.bat
```

This will:
- Kill any existing backend processes
- Verify environment configuration
- Start backend on http://localhost:8000 with CORS enabled

### Step 2: Verify Backend is Running
```bash
python test_cors_complete.py
```

Expected output:
```
✓ Status: 200
✓ All required CORS headers present
✓ Access-Control-Allow-Origin header is present
✓ ALL CORS TESTS PASSED!
```

### Step 3: Verify Frontend Configuration
Check `frontend/.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Step 4: Clear Browser Cache
1. Open DevTools (F12)
2. Right-click refresh button
3. Select "Empty Cache and Hard Reload"

OR

Press: `Ctrl + Shift + Delete` → Clear cache

### Step 5: Restart Frontend
```bash
cd frontend
npm run dev
```

## Quick Test

Open browser console and run:
```javascript
fetch('http://localhost:8000/health')
  .then(r => r.json())
  .then(d => console.log('✓ Backend accessible:', d))
  .catch(e => console.error('✗ Backend error:', e))
```

## If Still Not Working

### Check 1: Backend Port
```bash
netstat -ano | findstr :8000
```
Should show a process listening on port 8000

### Check 2: Backend Logs
Look at the backend terminal window for errors

### Check 3: Firewall
Windows Firewall might be blocking localhost connections:
```bash
netsh advfirewall firewall add rule name="Allow Port 8000" dir=in action=allow protocol=TCP localport=8000
```

### Check 4: Different Browser
Try in incognito mode or different browser to rule out cache issues

## Current CORS Configuration

Backend (`backend/main.py`):
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)
```

This is the most permissive CORS configuration for development.

## Production Note

For production, replace `allow_origins=["*"]` with specific domains:
```python
allow_origins=[
    "https://yourdomain.com",
    "https://www.yourdomain.com"
]
```
