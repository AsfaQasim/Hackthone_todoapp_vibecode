@echo off
echo ========================================
echo RESTARTING BACKEND WITH CORS FIX
echo ========================================
echo.

echo Step 1: Stopping any running backend processes...
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *uvicorn*" 2>nul
taskkill /F /IM python.exe /FI "WINDOWTITLE eq *main.py*" 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Step 2: Starting backend with CORS configuration...
cd backend
start "Backend Server" cmd /k "python main.py"

echo.
echo Step 3: Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo Step 4: Testing CORS configuration...
cd ..
python test_cors.py

echo.
echo ========================================
echo Backend restarted with CORS fix!
echo Backend URL: http://localhost:8000
echo ========================================
echo.
echo Now restart your frontend:
echo   cd frontend
echo   npm run dev
echo.
pause
