@echo off
echo Stopping containers...
docker-compose down

echo Building and starting containers...
docker-compose up -d --build

echo Waiting 10 seconds...
timeout /t 10 /nobreak

echo Checking status...
docker ps

echo.
echo Checking backend logs...
docker logs ai-chatbot-backend --tail 20

echo.
echo Done! Check http://localhost:3000 for frontend
echo Check http://localhost:8000/health for backend
