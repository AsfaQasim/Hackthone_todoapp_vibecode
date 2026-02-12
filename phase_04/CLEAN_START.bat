@echo off
echo Stopping all containers...
docker stop sleepy_colden affectionate_cori brave_hamilton ai-chatbot-backend ai-chatbot-frontend 2>nul
docker rm sleepy_colden affectionate_cori brave_hamilton ai-chatbot-backend ai-chatbot-frontend 2>nul

echo Starting fresh...
docker-compose down
docker-compose up -d

echo Waiting 10 seconds...
timeout /t 10 /nobreak

echo Checking status...
docker ps

echo.
echo Testing backend...
curl http://localhost:8000/health

echo.
echo Testing frontend...
curl http://localhost:3000

echo.
echo Done!
