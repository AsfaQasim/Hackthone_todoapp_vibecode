@echo off
echo ========================================
echo RESTART EVERYTHING - COMPLETE FIX
echo ========================================
echo.
echo STEP 1: Stop everything
echo ------------------------
echo 1. Go to BACKEND terminal and press Ctrl+C
echo 2. Go to FRONTEND terminal and press Ctrl+C
echo 3. Wait 5 seconds
echo.
pause
echo.
echo STEP 2: Start Backend
echo ---------------------
echo Opening backend in new window...
start cmd /k "cd backend && echo Starting Backend... && python -m uvicorn main:app --reload"
echo.
echo Wait for "Application startup complete" message
timeout /t 5
echo.
echo STEP 3: Test Backend
echo --------------------
python test_exact_frontend_call.py
echo.
echo Did you see "Tasks returned: 3"? (Y/N)
set /p BACKEND_OK=
if /i "%BACKEND_OK%"=="N" (
    echo.
    echo Backend not working! Close the backend window and try again.
    pause
    exit
)
echo.
echo STEP 4: Start Frontend
echo ----------------------
echo Opening frontend in new window...
start cmd /k "cd frontend && echo Starting Frontend... && npm run dev"
echo.
echo Wait for "Ready" message, then:
echo 1. Open browser: http://localhost:3000/general-task-execution
echo 2. You should see 3 tasks!
echo.
echo ========================================
echo DONE! Check your browser now.
echo ========================================
pause
