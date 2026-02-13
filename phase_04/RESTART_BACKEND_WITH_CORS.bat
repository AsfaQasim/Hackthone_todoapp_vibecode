@echo off
echo ========================================
echo Restarting Backend with CORS Fix
echo ========================================
echo.

echo Step 1: Finding and killing backend process...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do (
    echo Killing process %%a
    taskkill /F /PID %%a 2>nul
)

echo.
echo Step 2: Waiting 2 seconds...
timeout /t 2 /nobreak >nul

echo.
echo Step 3: Starting backend with CORS enabled...
cd backend
start "Backend Server" cmd /k "python main.py"

echo.
echo Step 4: Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo Step 5: Testing CORS...
cd ..
python test_cors_connection.py

echo.
echo ========================================
echo Backend restarted!
echo ========================================
echo.
echo Now test in browser:
echo 1. Go to http://localhost:3000/general-task-execution
echo 2. Open DevTools (F12) and check Console
echo 3. You should see tasks loading without CORS errors
echo.
pause
