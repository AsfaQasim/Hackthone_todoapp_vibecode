@echo off
echo Getting Minikube IP...
for /f "tokens=*" %%i in ('minikube ip') do set MINIKUBE_IP=%%i
echo Minikube IP: %MINIKUBE_IP%

echo.
echo Getting Backend NodePort...
for /f "tokens=*" %%i in ('kubectl get svc todo-chat-bot-backend -o jsonpath^="{.spec.ports[0].nodePort}"') do set BACKEND_PORT=%%i
echo Backend Port: %BACKEND_PORT%

echo.
echo Getting Frontend NodePort...
for /f "tokens=*" %%i in ('kubectl get svc todo-chat-bot-frontend -o jsonpath^="{.spec.ports[0].nodePort}"') do set FRONTEND_PORT=%%i
echo Frontend Port: %FRONTEND_PORT%

echo.
echo ========================================
echo YOUR APPLICATION URLS:
echo ========================================
echo.
echo Backend API:  http://%MINIKUBE_IP%:%BACKEND_PORT%
echo Backend Docs: http://%MINIKUBE_IP%:%BACKEND_PORT%/docs
echo.
echo Frontend:     http://%MINIKUBE_IP%:%FRONTEND_PORT%
echo.
echo ========================================

echo.
echo Opening Backend in browser...
start http://%MINIKUBE_IP%:%BACKEND_PORT%/docs

echo.
echo Opening Frontend in browser...
start http://%MINIKUBE_IP%:%FRONTEND_PORT%

echo.
pause
