@echo off
echo Deploying application...
helm install todo-chat-bot ./todo-chat-bot

echo.
echo Waiting 15 seconds...
timeout /t 15 /nobreak

echo.
echo Checking pods...
kubectl get pods

echo.
echo Checking services...
kubectl get services

echo.
echo Getting URLs...
minikube service list

echo.
pause
