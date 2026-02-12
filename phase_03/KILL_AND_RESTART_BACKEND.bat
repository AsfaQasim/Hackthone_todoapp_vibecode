@echo off
echo ========================================
echo KILLING ALL PYTHON AND RESTARTING
echo ========================================
echo.
echo Step 1: Killing all Python processes...
taskkill /F /IM python.exe 2>nul
if %errorlevel% == 0 (
    echo ✅ Python killed
) else (
    echo ℹ️ No Python running
)
echo.
echo Step 2: Waiting 3 seconds...
timeout /t 3 /nobreak >nul
echo.
echo Step 3: Clearing Python cache...
cd backend
for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" 2>nul
del /s /q *.pyc 2>nul
echo ✅ Cache cleared
echo.
echo Step 4: Starting backend...
echo ========================================
echo BACKEND STARTING - WAIT FOR STARTUP
echo ========================================
echo.
python -m uvicorn main:app --reload
