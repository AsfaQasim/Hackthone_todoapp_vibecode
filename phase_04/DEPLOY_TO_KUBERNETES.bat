@echo off
echo ========================================
echo AI Chatbot - Kubernetes Deployment
echo ========================================
echo.

echo Step 1: Loading images into Minikube...
minikube image load ai-chatbot-backend:latest
minikube image load ai-chatbot-frontend:latest

echo.
echo Step 2: Verifying images in Minikube...
minikube image ls | findstr ai-chatbot

echo.
echo Step 3: Installing Helm chart...
helm install todo-chat-bot ./todo-chat-bot

echo.
echo Step 4: Waiting for pods to be ready...
timeout /t 10 /nobreak

echo.
echo Step 5: Checking deployment status...
kubectl get pods
kubectl get services

echo.
echo Step 6: Getting service URLs...
echo.
echo Backend Service:
minikube service todo-chat-bot-backend --url

echo.
echo Frontend Service:
minikube service todo-chat-bot-frontend --url

echo.
echo ========================================
echo Deployment Complete!
echo ========================================
echo.
echo To access services:
echo   Backend:  minikube service todo-chat-bot-backend
echo   Frontend: minikube service todo-chat-bot-frontend
echo.
echo To check logs:
echo   kubectl logs -l app.kubernetes.io/component=backend
echo   kubectl logs -l app.kubernetes.io/component=frontend
echo.
pause
