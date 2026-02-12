@echo off
echo ========================================
echo Fresh Minikube Setup
echo ========================================

echo.
echo Step 1: Deleting old cluster...
minikube delete

echo.
echo Step 2: Starting fresh Minikube cluster...
minikube start --driver=docker --memory=4096 --cpus=2

echo.
echo Step 3: Verifying cluster...
minikube status

echo.
echo Step 4: Testing kubectl...
kubectl get nodes

echo.
echo Step 5: Loading images...
minikube image load ai-chatbot-backend:latest
minikube image load ai-chatbot-frontend:latest

echo.
echo Step 6: Deploying application...
helm install todo-chat-bot ./todo-chat-bot

echo.
echo Step 7: Waiting for pods...
timeout /t 20 /nobreak

echo.
echo Step 8: Checking deployment...
kubectl get pods
kubectl get services

echo.
echo Step 9: Getting service URLs...
echo.
echo Backend:
minikube service todo-chat-bot-backend --url

echo.
echo Frontend:
minikube service todo-chat-bot-frontend --url

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
pause
