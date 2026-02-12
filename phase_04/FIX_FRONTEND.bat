@echo off
echo Rebuilding frontend with correct backend URL...
docker-compose down
docker-compose up -d --build

echo.
echo Waiting 15 seconds...
timeout /t 15 /nobreak

echo.
echo Checking status...
docker ps

echo.
echo Testing backend...
curl http://localhost:8000/health

echo.
echo ========================================
echo Services Ready!
echo ========================================
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Opening frontend...
start http://localhost:3000

pause
