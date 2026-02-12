@echo off
echo Starting Minikube with Docker driver...
echo.

REM Stop existing minikube if running
minikube stop 2>nul
minikube delete 2>nul

echo.
echo Starting fresh Minikube cluster with Docker...
minikube start --driver=docker

echo.
echo Checking Minikube status...
minikube status

echo.
echo Checking Docker containers...
docker ps | findstr minikube

echo.
echo ========================================
echo Minikube is running in Docker!
echo ========================================
echo.
echo Useful commands:
echo   minikube status
echo   minikube dashboard
echo   kubectl get nodes
echo   docker ps
echo.
pause
