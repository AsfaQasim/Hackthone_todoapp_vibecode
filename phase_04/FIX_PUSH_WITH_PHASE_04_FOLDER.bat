@echo off
echo ========================================
echo Phase_04 Folder Ke Saath Push Karna
echo ========================================
echo.

echo Step 1: Parent directory mein ja rahe hain...
cd /d F:\hackthone_todo_vibecode

echo.
echo Step 2: Agar .git hai to delete kar rahe hain...
if exist .git (
    echo Removing old .git folder...
    rmdir /s /q .git
)

echo.
echo Step 3: Git initialize kar rahe hain...
git init

echo.
echo Step 4: Remote add kar rahe hain...
git remote add origin https://github.com/AsfaQasim/Hackthone_todoapp_vibecode.git

echo.
echo Step 5: .gitignore bana rahe hain...
(
    echo .env
    echo .env.local
    echo .env.*.local
    echo .env.docker
    echo node_modules/
    echo __pycache__/
    echo *.pyc
    echo .pytest_cache/
    echo *.db
    echo .DS_Store
    echo **/__pycache__/
    echo **/.next/
    echo **/node_modules/
) > .gitignore

echo.
echo Step 6: Sirf phase_04 folder add kar rahe hain...
git add phase_04/
git add .gitignore

echo.
echo Step 7: Commit kar rahe hain...
git commit -m "feat: Add phase_04 folder with Docker setup

- Backend with FastAPI and Docker
- Frontend with Next.js and Docker
- Docker Compose orchestration
- Environment variables management"

echo.
echo Step 8: Main branch set kar rahe hain...
git branch -M main

echo.
echo Step 9: Push kar rahe hain...
git push -u origin main --force

echo.
echo ========================================
echo Done! Phase_04 folder pushed to GitHub
echo ========================================
echo.
echo GitHub structure:
echo phase_04/
echo   ├── backend/
echo   ├── frontend/
echo   ├── docker-compose.yml
echo   └── ...
echo.
pause
