@echo off
echo Starting Port Forwarding...
echo.
echo Backend will be available at: http://localhost:8000
echo Frontend will be available at: http://localhost:3000
echo.
echo Press CTRL+C to stop
echo.

start "Backend Port Forward" cmd /k "kubectl port-forward svc/todo-chat-bot-backend 8000:8000"
timeout /t 2 /nobreak

start "Frontend Port Forward" cmd /k "kubectl port-forward svc/todo-chat-bot-frontend 3000:3000"
timeout /t 3 /nobreak

echo.
echo Opening services in browser...
start http://localhost:8000/docs
start http://localhost:3000

echo.
echo Services are running!
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Keep this window open!
pause
