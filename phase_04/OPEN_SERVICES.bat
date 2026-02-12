@echo off
echo Opening Backend Service...
start cmd /k "minikube service todo-chat-bot-backend"

timeout /t 3 /nobreak

echo Opening Frontend Service...
start cmd /k "minikube service todo-chat-bot-frontend"

echo.
echo Services are opening in browser!
echo.
pause
