@echo off
echo ========================================
echo Switching to Docker Compose
echo ========================================

echo.
echo Step 1: Stopping Kubernetes deployment...
helm uninstall todo-chat-bot 2>nul

echo.
echo Step 2: Starting Docker Compose...
docker-compose down
docker-compose up -d

echo.
echo Step 3: Waiting for services...
timeout /t 10 /nobreak

echo.
echo Step 4: Checking status...
docker ps

echo.
echo Step 5: Testing backend...
curl http://localhost:8000/health

echo.
echo ========================================
echo Services Ready!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Backend Docs: http://localhost:8000/docs
echo Frontend: http://localhost:3000
echo.
echo Opening in browser...
start http://localhost:3000
start http://localhost:8000/docs

echo.
pause
