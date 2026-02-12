@echo off
echo ========================================
echo FORCE RESTART BACKEND - KILL ALL PYTHON
echo ========================================
echo.
echo This will:
echo 1. Kill all Python processes
echo 2. Clear Python cache
echo 3. Start backend fresh
echo.
pause
echo.
echo Step 1: Killing all Python processes...
taskkill /F /IM python.exe 2>nul
if %errorlevel% == 0 (
    echo ✅ Python processes killed
) else (
    echo ℹ️ No Python processes found
)
echo.
echo Step 2: Waiting 3 seconds...
timeout /t 3 /nobreak >nul
echo.
echo Step 3: Starting backend...
cd backend
echo.
echo ========================================
echo Backend starting now...
echo Wait for "Application startup complete"
echo ========================================
echo.
python -m uvicorn main:app --reload
