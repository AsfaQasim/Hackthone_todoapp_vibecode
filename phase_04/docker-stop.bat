@echo off
REM Docker Stop Script for AI Chatbot Application

echo ========================================
echo Stopping AI Chatbot Application
echo ========================================
echo.

docker-compose down

if errorlevel 1 (
    echo ERROR: Failed to stop services!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Application Stopped Successfully!
echo ========================================
echo.

pause
