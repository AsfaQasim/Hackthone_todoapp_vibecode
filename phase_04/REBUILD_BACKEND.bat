@echo off
echo ========================================
echo Rebuilding Backend Container
echo ========================================
echo.

echo Step 1: Stopping backend container...
docker-compose stop backend
echo.

echo Step 2: Rebuilding backend with updated OpenAI...
docker-compose build backend --no-cache
echo.

echo Step 3: Starting backend container...
docker-compose up -d backend
echo.

echo Step 4: Waiting for backend to start (15 seconds)...
timeout /t 15 /nobreak
echo.

echo Step 5: Checking backend logs...
docker logs ai-chatbot-backend --tail 30
echo.

echo ========================================
echo Backend Rebuild Complete!
echo ========================================
echo.
echo Backend: http://localhost:8000
echo Backend Docs: http://localhost:8000/docs
echo.
echo Changes applied:
echo   - Updated OpenAI to version 1.54.0
echo   - Fixes httpx proxies compatibility issue
echo   - AI function calling should now work
echo.
pause
