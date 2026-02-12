@echo off
echo ========================================
echo RESTARTING BACKEND WITH FIXES
echo ========================================
echo.
echo Please follow these steps:
echo.
echo 1. Go to your backend terminal
echo 2. Press Ctrl+C to stop the backend
echo 3. Run: cd backend
echo 4. Run: python -m uvicorn main:app --reload
echo.
echo After backend restarts, test with:
echo    python test_backend_tasks.py
echo.
pause
