@echo off
echo ========================================
echo COMPLETE CORS FIX - STEP BY STEP
echo ========================================
echo.

echo Step 1: Diagnosing current state...
python diagnose_cors_issue.py

echo.
echo ========================================
echo Step 2: Stopping all services...
echo ========================================
taskkill /F /IM node.exe 2>nul
taskkill /F /IM python.exe 2>nul
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo Step 3: Starting Backend...
echo ========================================
cd backend
start "Backend Server" cmd /k "echo Starting Backend... && python main.py"
cd ..

echo Waiting for backend to start...
timeout /t 8 /nobreak >nul

echo.
echo ========================================
echo Step 4: Testing Backend...
echo ========================================
python -c "import requests; r = requests.get('http://localhost:8000/health'); print('Backend Status:', r.status_code, r.json())"

echo.
echo ========================================
echo Step 5: Starting Frontend...
echo ========================================
cd frontend
start "Frontend Server" cmd /k "echo Starting Frontend... && npm run dev"
cd ..

echo Waiting for frontend to start...
timeout /t 10 /nobreak >nul

echo.
echo ========================================
echo SERVICES STARTED!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Now open: http://localhost:3000/general-task-execution
echo.
echo If you still see CORS error:
echo 1. Open Browser DevTools (F12)
echo 2. Go to Network tab
echo 3. Try to load tasks
echo 4. Look for the failed request
echo 5. Check if URL is /api/tasks or localhost:8000
echo.
pause
