@echo off
echo ========================================
echo Testing Docker Deployment
echo ========================================
echo.

echo Test 1: Checking if containers are running...
docker ps --filter "name=ai-chatbot" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
echo.

echo Test 2: Testing backend health endpoint...
curl -s http://localhost:8000/health
echo.
echo.

echo Test 3: Testing backend docs endpoint...
curl -s -o nul -w "Status: %%{http_code}\n" http://localhost:8000/docs
echo.

echo Test 4: Testing frontend homepage...
curl -s -o nul -w "Status: %%{http_code}\n" http://localhost:3000
echo.

echo Test 5: Checking backend logs for errors...
echo Last 10 lines of backend logs:
docker logs ai-chatbot-backend --tail 10
echo.

echo Test 6: Checking frontend logs for errors...
echo Last 10 lines of frontend logs:
docker logs ai-chatbot-frontend --tail 10
echo.

echo ========================================
echo Test Complete!
echo ========================================
echo.
echo If all tests passed:
echo   - Backend should show "Status: 200" for health and docs
echo   - Frontend should show "Status: 200"
echo   - No error messages in logs
echo.
echo You can now test the application:
echo   1. Open http://localhost:3000 in your browser
echo   2. Try to sign up or login
echo   3. Create a task
echo   4. Test the chat feature
echo.
pause
