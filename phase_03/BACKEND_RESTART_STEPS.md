# Backend Restart - Step by Step

## Issue
Login still failing with 500 error even after config fix.

## Complete Backend Restart Steps

### Step 1: Stop Backend Completely
```bash
# In backend terminal, press Ctrl+C
# If that doesn't work, kill the process:
taskkill /F /IM python.exe
```

### Step 2: Verify Backend is Stopped
```bash
curl http://localhost:8000/health
# Should give connection error (good - means it's stopped)
```

### Step 3: Check Environment File
```bash
cd backend
type .env
```

Verify these lines exist:
```env
DATABASE_URL=postgresql://neondb_owner:npg_6DzBwoCp1Muf@ep-holy-flower-ahrkffp6-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require
BETTER_AUTH_SECRET=dea0238a9436145d14499ff6aeddb80870c4738f7268efec87b7acdff0589e066
```

### Step 4: Delete Python Cache
```bash
cd backend
rmdir /s /q __pycache__
rmdir /s /q src\__pycache__
del *.pyc
```

### Step 5: Start Backend Fresh
```bash
cd backend
python main.py
```

### Step 6: Watch Startup Logs

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
Starting AI Chatbot MCP...
Database tables created successfully  ← IMPORTANT!
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**If you see:**
```
❌ Error creating database tables: ...
```
Then there's a database connection issue.

### Step 7: Test Health Endpoint
```bash
curl http://localhost:8000/health
```

Expected:
```json
{"status":"healthy","service":"AI Chatbot with MCP"}
```

### Step 8: Test Login
```bash
curl -X POST http://localhost:8000/login -H "Content-Type: application/json" -d "{\"email\":\"test@test.com\",\"password\":\"test\"}"
```

Expected:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user_id": "..."
}
```

## If Still Getting 500 Error

### Check Backend Terminal for Errors

Look for these error patterns:

#### Error 1: Database Connection
```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solution:**
- Check Neon dashboard - is database active?
- Check DATABASE_URL is correct
- Check internet connection

#### Error 2: Missing Module
```
ModuleNotFoundError: No module named 'xxx'
```

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

#### Error 3: Import Error
```
ImportError: cannot import name 'xxx'
```

**Solution:**
```bash
cd backend
rmdir /s /q __pycache__
python main.py
```

#### Error 4: Table Missing
```
sqlalchemy.exc.ProgrammingError: relation "user" does not exist
```

**Solution:**
```bash
cd backend
python -c "from src.db import init_db; init_db()"
python main.py
```

## Alternative: Use SQLite for Testing

If Neon database is causing issues, temporarily use SQLite:

### Step 1: Edit backend/.env
```env
# Comment out Neon URL
# DATABASE_URL=postgresql://...

# Add SQLite URL
DATABASE_URL=sqlite:///./todo_app_local.db
```

### Step 2: Restart Backend
```bash
cd backend
python main.py
```

### Step 3: Test Login
```bash
curl -X POST http://localhost:8000/login -H "Content-Type: application/json" -d "{\"email\":\"test@test.com\",\"password\":\"test\"}"
```

Should work with SQLite!

## Debug: Check What Database Backend is Using

Run this in backend terminal:
```bash
cd backend
python -c "from src.config import settings; print('Database:', settings.database_url)"
```

Should show:
```
Database: postgresql://neondb_owner:...
```

If it shows SQLite, config is not loading correctly.

## Share These Logs

If still not working, share:

1. **Backend startup logs** (full output when you run `python main.py`)
2. **Error when testing login** (what backend terminal shows when you curl /login)
3. **Database check output:**
```bash
cd backend
python -c "from src.config import settings; print(settings.database_url)"
```

This will help identify the exact issue!
