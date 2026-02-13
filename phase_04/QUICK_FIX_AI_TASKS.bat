@echo off
echo ================================================================================
echo QUICK FIX FOR AI TASKS "Failed to fetch" ERROR
echo ================================================================================
echo.

echo Step 1: Checking if backend is running...
curl -s http://localhost:8000/health
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Backend is NOT running!
    echo.
    echo Starting backend...
    start cmd /k "cd backend && python main.py"
    timeout /t 5
) else (
    echo ✅ Backend is running!
)

echo.
echo Step 2: Testing AI tasks endpoint...
python test_ai_tasks_with_user.py

echo.
echo Step 3: Checking if frontend is running...
curl -s http://localhost:3000 > nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Frontend is NOT running!
    echo.
    echo Starting frontend...
    start cmd /k "cd frontend && npm run dev"
    echo.
    echo ⏳ Wait for frontend to start (about 10-20 seconds)
    echo    Then open: http://localhost:3000
) else (
    echo ✅ Frontend is running!
)

echo.
echo ================================================================================
echo NEXT STEPS:
echo ================================================================================
echo 1. Open http://localhost:3000 in your browser
echo 2. Log out and log in again
echo 3. Go to AI Tasks page
echo 4. You should see your task!
echo.
echo If still not working:
echo - Press F12 in browser
echo - Go to Console tab
echo - Take a screenshot of any errors
echo ================================================================================
pause
