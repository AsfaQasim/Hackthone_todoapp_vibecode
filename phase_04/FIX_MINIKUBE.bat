@echo off
echo Stopping Minikube...
minikube stop

echo.
echo Starting Minikube with Docker driver...
minikube start --driver=docker

echo.
echo Checking status...
minikube status

echo.
echo Testing kubectl connection...
kubectl get nodes

echo.
echo Minikube is ready!
pause
