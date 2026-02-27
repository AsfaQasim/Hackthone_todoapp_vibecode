@echo off
echo ========================================
echo Login Issue Diagnostic Tool
echo ========================================
echo.

echo Step 1: Checking if Backend is running...
curl -s http://localhost:8000/health
if %errorlevel% equ 0 (
    echo ✅ Backend is running!
) else (
    echo ❌ Backend is NOT running!
    echo.
    echo Please start backend:
    echo   cd backend
    echo   python main.py
    goto :end
)

echo.
echo Step 2: Testing login endpoint...
curl -X POST http://localhost:8000/login -H "Content-Type: application/json" -d "{\"email\":\"test@test.com\",\"password\":\"test\"}"

echo.
echo.
echo Step 3: Checking frontend...
curl -s http://localhost:3000 >nul
if %errorlevel% equ 0 (
    echo ✅ Frontend is running!
) else (
    echo ❌ Frontend is NOT running!
    echo.
    echo Please start frontend:
    echo   cd frontend
    echo   npm run dev
)

echo.
echo ========================================
echo Diagnostic Complete!
echo ========================================
echo.
echo If backend is not running, start it with:
echo   cd backend
echo   python main.py
echo.
echo If frontend is not running, start it with:
echo   cd frontend
echo   npm run dev
echo.

:end
pause
