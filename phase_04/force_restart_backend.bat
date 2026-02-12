@echo off
echo ========================================
echo BACKEND RESTART SCRIPT
echo ========================================
echo.
echo Killing any existing Python processes...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul
echo.
echo Starting backend...
cd backend
start cmd /k "python -m uvicorn main:app --reload"
echo.
echo Backend starting in new window...
echo Wait 5 seconds for it to start...
timeout /t 5 /nobreak
echo.
echo Testing backend...
curl http://localhost:8000/health
echo.
echo ========================================
echo Backend should be running now!
echo ========================================
pause
