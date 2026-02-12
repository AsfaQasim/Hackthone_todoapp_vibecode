@echo off
echo Loading backend image...
minikube image load ai-chatbot-backend:latest

echo Loading frontend image...
minikube image load ai-chatbot-frontend:latest

echo Installing Helm chart...
helm install todo-chat-bot ./todo-chat-bot

echo.
echo Checking pods...
kubectl get pods

echo.
echo Checking services...
kubectl get services

echo.
echo Done!
pause
