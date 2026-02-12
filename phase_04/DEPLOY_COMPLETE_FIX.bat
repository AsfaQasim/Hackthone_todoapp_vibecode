@echo off
cls
echo ========================================
echo COMPLETE FIX DEPLOYMENT
echo ========================================
echo.
echo This will:
echo 1. Stop all containers
echo 2. Rebuild both backend and frontend
echo 3. Start everything fresh
echo.
pause

echo Step 1: Stopping containers...
docker-compose down
echo.

echo Step 2: Building backend...
docker-compose build backend
echo.

echo Step 3: Building frontend...
docker-compose build frontend
echo.

echo Step 4: Starting all services...
docker-compose up -d
echo.

echo Step 5: Waiting 20 seconds for startup...
timeout /t 20 /nobreak
echo.

echo Step 6: Checking status...
docker ps --filter "name=ai-chatbot"
echo.

echo Step 7: Testing backend...
curl -s http://localhost:8000/health
echo.
echo.

echo ========================================
echo DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo Services:
echo   Frontend: http://localhost:3000
echo   Backend: http://localhost:8000
echo.
echo What's Fixed:
echo   ✅ Auth middleware now processes tokens for tasks endpoints
echo   ✅ General-task-execution uses correct API endpoint
echo   ✅ Tasks page loads tasks on mount
echo   ✅ Chat creates tasks with correct schema
echo.
echo Test Steps:
echo   1. Go to http://localhost:3000
echo   2. Login with: asfaqasim145@gmail.com
echo   3. Go to chat and say: "add task: test task"
echo   4. Go to "AI Tasks" page - should see your task!
echo.
pause
