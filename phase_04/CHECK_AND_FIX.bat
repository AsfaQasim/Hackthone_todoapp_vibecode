@echo off
echo Checking pod status...
kubectl get pods

echo.
echo Checking pod logs - Backend...
kubectl logs -l app.kubernetes.io/component=backend --tail=20

echo.
echo Checking pod logs - Frontend...
kubectl logs -l app.kubernetes.io/component=frontend --tail=20

echo.
echo Checking services...
kubectl get services -o wide

echo.
echo Getting service URLs...
kubectl get svc todo-chat-bot-backend -o jsonpath='{.spec.ports[0].nodePort}'
echo.
kubectl get svc todo-chat-bot-frontend -o jsonpath='{.spec.ports[0].nodePort}'
echo.

echo.
echo Describing backend service...
kubectl describe svc todo-chat-bot-backend

echo.
echo Describing frontend service...
kubectl describe svc todo-chat-bot-frontend

echo.
pause
