@echo off
echo ========================================
echo Docker Deployment - Fixed Version
echo ========================================
echo.

echo Step 1: Stopping all containers...
docker-compose down
echo.

echo Step 2: Removing old images (optional - comment out if you want to keep them)...
REM docker rmi phase_04-backend:latest phase_04-frontend:latest 2>nul
echo Skipping image removal...
echo.

echo Step 3: Building fresh images with latest code...
echo Building backend...
docker-compose build backend
echo.
echo Building frontend...
docker-compose build frontend
echo.

echo Step 4: Starting containers in detached mode...
docker-compose up -d
echo.

echo Step 5: Waiting for services to initialize (15 seconds)...
timeout /t 15 /nobreak
echo.

echo Step 6: Checking container status...
docker ps --filter "name=ai-chatbot"
echo.

echo Step 7: Checking backend health...
echo Waiting for backend to be ready...
timeout /t 5 /nobreak
curl -s http://localhost:8000/health
echo.
echo.

echo Step 8: Checking backend logs (last 30 lines)...
docker logs ai-chatbot-backend --tail 30
echo.

echo Step 9: Checking frontend logs (last 30 lines)...
docker logs ai-chatbot-frontend --tail 30
echo.

echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo Services:
echo   Backend API: http://localhost:8000
echo   Backend Docs: http://localhost:8000/docs
echo   Frontend: http://localhost:3000
echo.
echo To view live logs:
echo   Backend:  docker logs ai-chatbot-backend -f
echo   Frontend: docker logs ai-chatbot-frontend -f
echo.
echo To stop services:
echo   docker-compose down
echo.
echo Key Changes Applied:
echo   - All API routes now use BACKEND_URL for container-to-container communication
echo   - Frontend connects to backend via Docker network (http://backend:8000)
echo   - Browser connects to frontend via localhost:3000
echo.
pause
