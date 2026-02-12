@echo off
echo ========================================
echo Starting All Containers
echo ========================================
echo.

echo Stopping any running containers...
docker-compose down
echo.

echo Starting backend and frontend...
docker-compose up -d
echo.

echo Waiting 15 seconds for services to start...
timeout /t 15 /nobreak
echo.

echo Checking container status...
docker ps --filter "name=ai-chatbot"
echo.

echo Checking backend health...
curl -s http://localhost:8000/health
echo.
echo.

echo ========================================
echo Services Started!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
pause
