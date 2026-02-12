@echo off
echo ========================================
echo Rebuilding Frontend Container
echo ========================================
echo.

echo Step 1: Stopping frontend container...
docker-compose stop frontend
echo.

echo Step 2: Rebuilding frontend with latest code...
docker-compose build frontend
echo.

echo Step 3: Starting frontend container...
docker-compose up -d frontend
echo.

echo Step 4: Waiting for frontend to start (10 seconds)...
timeout /t 10 /nobreak
echo.

echo Step 5: Checking frontend logs...
docker logs ai-chatbot-frontend --tail 20
echo.

echo ========================================
echo Frontend Rebuild Complete!
echo ========================================
echo.
echo Frontend: http://localhost:3000
echo.
echo Changes applied:
echo   - Added /api/health proxy route
echo   - ChatInterface now uses proxy for health check
echo   - Fixes Docker networking issue
echo.
pause
