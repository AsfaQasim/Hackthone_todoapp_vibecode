@echo off
echo Cleaning everything...
docker stop $(docker ps -aq) 2>nul
docker rm $(docker ps -aq) 2>nul
docker-compose down -v

echo Starting with docker-compose...
docker-compose up -d --force-recreate

timeout /t 15

echo Checking containers...
docker ps

echo.
echo Testing backend health...
curl http://localhost:8000/health

echo.
pause
