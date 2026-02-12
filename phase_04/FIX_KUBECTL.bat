@echo off
echo Fixing kubectl configuration...

echo.
echo Step 1: Update Minikube context...
minikube update-context

echo.
echo Step 2: Set kubectl context to minikube...
kubectl config use-context minikube

echo.
echo Step 3: Verify connection...
kubectl get nodes

echo.
echo Step 4: Check cluster info...
kubectl cluster-info

echo.
echo Configuration fixed!
echo.
echo Now deploy with:
echo   DEPLOY_NOW.bat
echo.
pause
