@echo off
echo ========================================
echo COMPLETE CORS FIX - Backend Restart
echo ========================================
echo.

echo Step 1: Stopping any running backend processes...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM uvicorn.exe 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Step 2: Verifying backend environment...
cd backend
if not exist .env (
    echo ERROR: backend/.env not found!
    pause
    exit /b 1
)

echo.
echo Step 3: Installing/updating dependencies...
pip install -q fastapi uvicorn python-jose[cryptography] passlib[bcrypt] sqlalchemy pydantic-settings python-multipart openai

echo.
echo Step 4: Starting backend with CORS enabled...
echo Backend will run on http://localhost:8000
echo Frontend should use: http://localhost:3000
echo.
echo CORS Configuration:
echo - Allowed Origins: * (all origins)
echo - Allowed Methods: GET, POST, PUT, DELETE, OPTIONS, PATCH
echo - Allowed Headers: * (all headers)
echo.

start "Backend Server" cmd /k "python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

echo.
echo Step 5: Waiting for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo Step 6: Testing backend health...
curl -s http://localhost:8000/health

echo.
echo ========================================
echo Backend is running!
echo ========================================
echo.
echo Test URLs:
echo - Health: http://localhost:8000/health
echo - Docs: http://localhost:8000/docs
echo.
echo Now start your frontend with: npm run dev
echo.
pause
