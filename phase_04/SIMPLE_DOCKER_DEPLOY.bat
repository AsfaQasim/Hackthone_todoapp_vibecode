@echo off
echo ========================================
echo Simple Docker Deployment
echo ========================================
echo.

echo Step 1: Stopping any running containers...
docker-compose down
echo.

echo Step 2: Building images...
docker-compose build
echo.

echo Step 3: Starting containers...
docker-compose up -d
echo.

echo Step 4: Waiting for services to start...
timeout /t 10 /nobreak
echo.

echo Step 5: Checking container status...
docker ps
echo.

echo Step 6: Checking backend logs...
docker logs ai-chatbot-backend --tail 20
echo.

echo Step 7: Checking frontend logs...
docker logs ai-chatbot-frontend --tail 20
echo.

echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Backend Docs: http://localhost:8000/docs
echo Frontend: http://localhost:3000
echo.
echo To check logs:
echo   docker logs ai-chatbot-backend -f
echo   docker logs ai-chatbot-frontend -f
echo.
pause
