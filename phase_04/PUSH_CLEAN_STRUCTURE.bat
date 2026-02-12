@echo off
echo ========================================
echo Clean Structure Push - Sirf Phase Folders
echo ========================================
echo.

echo Step 1: Current directory check...
cd /d F:\hackthone_todo_vibecode
cd
echo.

echo Step 2: Agar .git hai to delete kar rahe hain...
if exist .git (
    echo Removing old .git...
    rmdir /s /q .git
)

echo.
echo Step 3: Agar phase_04 ke andar .git hai to delete kar rahe hain...
if exist phase_04\.git (
    echo Removing .git from phase_04...
    rmdir /s /q phase_04\.git
)

echo.
echo Step 4: Git initialize kar rahe hain...
git init

echo.
echo Step 5: Remote add kar rahe hain...
git remote add origin https://github.com/AsfaQasim/Hackthone_todoapp_vibecode.git

echo.
echo Step 6: .gitignore bana rahe hain...
(
    echo # Environment files
    echo .env
    echo .env.local
    echo .env.*.local
    echo .env.docker
    echo.
    echo # Dependencies
    echo node_modules/
    echo.
    echo # Python
    echo __pycache__/
    echo *.pyc
    echo .pytest_cache/
    echo.
    echo # Database
    echo *.db
    echo.
    echo # OS
    echo .DS_Store
    echo.
    echo # Build outputs
    echo **/.next/
    echo **/dist/
    echo.
    echo # Ignore root level files/folders except phases
    echo /backend/
    echo /frontend/
    echo /my-app/
    echo /node_modules/
    echo /specs/
    echo /history/
    echo /todo-chat-bot/
    echo /*.py
    echo /*.js
    echo /*.md
    echo /*.bat
    echo /*.txt
    echo /*.yml
    echo /*.yaml
    echo /*.json
    echo /*.log
    echo /*.db
) > .gitignore

echo.
echo Step 7: SIRF phase folders add kar rahe hain...
git add phase_01/
git add phase_02/
git add phase_03/
git add phase_04/
git add .gitignore

echo.
echo Step 8: Git status check...
git status

echo.
echo Step 9: Commit kar rahe hain...
git commit -m "feat: Add all project phases with clean structure

Project Structure:
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
echo Done! Clean Structure Pushed to GitHub
echo ========================================
echo.
echo GitHub URL: https://github.com/AsfaQasim/Hackthone_todoapp_vibecode
echo.
echo GitHub Structure (Clean):
echo ├── phase_01/
echo ├── phase_02/
echo ├── phase_03/
echo └── phase_04/
echo.
echo Root level files are gitignored!
echo.
pause
