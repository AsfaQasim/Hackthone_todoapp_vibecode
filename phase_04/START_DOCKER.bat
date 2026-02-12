docker-compose down
docker-compose up -d
timeout /t 5
docker ps
echo.
echo Backend: http://localhost:8000/health
echo Frontend: http://localhost:3000
