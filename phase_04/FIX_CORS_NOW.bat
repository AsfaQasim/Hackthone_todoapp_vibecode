@echo off
echo ========================================
echo FIXING CORS ISSUE
echo ========================================
echo.

echo Step 1: Stopping backend if running...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *uvicorn*" 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Step 2: Backend .env updated with ALLOWED_ORIGINS=*
echo.

echo Step 3: Starting backend with CORS fix...
cd backend
start "Backend Server" cmd /k "python -m uvicorn main:app --reload --port 8000 --host 0.0.0.0"

echo.
echo Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo Step 4: Testing CORS...
curl -X OPTIONS http://localhost:8000/api/tasks -H "Origin: http://localhost:3000" -H "Access-Control-Request-Method: GET" -v

echo.
echo ========================================
echo CORS FIX COMPLETE!
echo ========================================
echo.
echo Backend is running on: http://localhost:8000
echo Frontend should now work without CORS errors
echo.
echo Test in browser:
echo 1. Open http://localhost:3000
echo 2. Login
echo 3. Go to /general-task-execution
echo 4. Tasks should load without CORS errors
echo.
pause
