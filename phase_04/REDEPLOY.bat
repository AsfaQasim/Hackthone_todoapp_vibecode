@echo off
echo Uninstalling old deployment...
helm uninstall todo-chat-bot

echo.
echo Waiting 5 seconds...
timeout /t 5 /nobreak

echo.
echo Installing updated chart...
helm install todo-chat-bot ./todo-chat-bot

echo.
echo Waiting 20 seconds for pods...
timeout /t 20 /nobreak

echo.
echo Checking status...
kubectl get pods
kubectl get services

echo.
echo Starting port forwarding...
start "Backend" cmd /k "kubectl port-forward svc/todo-chat-bot-backend 8000:8000"
timeout /t 2 /nobreak
start "Frontend" cmd /k "kubectl port-forward svc/todo-chat-bot-frontend 3000:3000"
timeout /t 3 /nobreak

echo.
echo Opening in browser...
start http://localhost:3000
start http://localhost:8000/docs

echo.
echo Done!
pause
