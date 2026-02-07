@echo off
echo ========================================
echo COMPLETE BACKEND FIX
echo ========================================
echo.

echo Step 1: Killing all Python processes...
taskkill /F /IM python.exe /T 2>nul
timeout /t 2 /nobreak >nul

echo Step 2: Clearing Python cache...
cd backend
del /s /q __pycache__ 2>nul
del /s /q routes\__pycache__ 2>nul
del /s /q src\__pycache__ 2>nul
del /s /q *.pyc 2>nul
cd ..

echo Step 3: Starting backend in new window...
cd backend
start "Backend Server" cmd /k "python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
cd ..

echo.
echo Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak >nul

echo.
echo Step 4: Testing backend...
python test_with_correct_user.py

echo.
echo ========================================
echo If you see "USER ID MATCHES", backend is fixed!
echo If not, check backend terminal for errors.
echo ========================================
pause
