@echo off
echo Checking Helm releases...
helm list

echo.
echo Checking pods...
kubectl get pods

echo.
echo Checking services...
kubectl get services

echo.
echo Checking all resources...
kubectl get all

echo.
echo Describing pods...
kubectl describe pods

echo.
pause
