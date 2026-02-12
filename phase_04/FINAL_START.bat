@echo off
cls
echo ========================================
echo Starting AI Chatbot Application
echo ========================================
echo.

echo Cleaning up...
docker-compose down 2>nul
echo.

echo Starting services...
docker-compose up -d
echo.

echo Waiting 25 seconds for services to initialize...
timeout /t 25 /nobreak >nul
echo.

echo Checking status...
docker ps --filter "name=ai-chatbot" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo.

echo Testing backend...
curl -s http://localhost:8000/health
echo.
echo.

echo ========================================
echo READY!
echo ========================================
echo.
echo Frontend: http://localhost:3000
echo Backend: http://localhost:8000
echo.
echo To create a task in chat, type:
echo   add task: my eating
echo.
echo (Use exact format with colon!)
echo.
pause
