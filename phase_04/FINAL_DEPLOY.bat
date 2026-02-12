@echo off
echo Installing Helm chart...
helm install todo-chat-bot ./todo-chat-bot

echo.
echo Waiting 20 seconds for pods to start...
timeout /t 20 /nobreak

echo.
echo ========================================
echo Deployment Status
echo ========================================

echo.
echo Pods:
kubectl get pods -o wide

echo.
echo Services:
kubectl get services

echo.
echo All Resources:
kubectl get all

echo.
echo ========================================
echo Service URLs
echo ========================================
minikube service list

echo.
echo To access services:
echo   minikube service todo-chat-bot-backend
echo   minikube service todo-chat-bot-frontend
echo.
pause
