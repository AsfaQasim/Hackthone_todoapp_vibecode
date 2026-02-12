@echo off
echo ========================================
echo Sab Phases Push Karna (phase_01 to phase_04)
echo ========================================
echo.

echo Step 1: Parent directory mein ja rahe hain...
cd /d F:\hackthone_todo_vibecode

echo.
echo Step 2: Current location:
cd
echo.

echo Step 3: Available phases check kar rahe hain...
dir /b | findstr phase

echo.
echo Step 4: Agar phase_04 ke andar .git hai to delete kar rahe hain...
if exist phase_04\.git (
    echo Removing .git from phase_04...
    rmdir /s /q phase_04\.git
)

echo.
echo Step 5: Parent directory mein git init kar rahe hain...
if exist .git (
    echo .git already exists, removing...
    rmdir /s /q .git
)
git init

echo.
echo Step 6: Remote add kar rahe hain...
git remote add origin https://github.com/AsfaQasim/Hackthone_todoapp_vibecode.git

echo.
echo Step 7: .gitignore bana rahe hain...
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
    echo **/.pytest_cache/
) > .gitignore

echo.
echo Step 8: SAB phases add kar rahe hain...
git add phase_01/
git add phase_02/
git add phase_03/
git add phase_04/
git add .gitignore

echo.
echo Step 9: Commit kar rahe hain...
git commit -m "feat: Add all project phases (phase_01 to phase_04)

- phase_01: Initial project setup
- phase_02: Authentication implementation
- phase_03: Task management features
- phase_04: Docker setup for frontend and backend

Complete AI Chatbot Todo App with MCP integration"

echo.
echo Step 10: Main branch set kar rahe hain...
git branch -M main

echo.
echo Step 11: Push kar rahe hain...
git push -u origin main --force

echo.
echo ========================================
echo Done! Sab Phases Pushed to GitHub
echo ========================================
echo.
echo GitHub URL: https://github.com/AsfaQasim/Hackthone_todoapp_vibecode
echo.
echo Expected structure:
echo ├── phase_01/
echo ├── phase_02/
echo ├── phase_03/
echo └── phase_04/
echo.
pause
