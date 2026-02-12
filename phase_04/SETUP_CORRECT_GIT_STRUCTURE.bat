@echo off
echo ========================================
echo Correct Git Structure Setup
echo ========================================
echo.

echo Current Situation:
echo - Git repo shayad phase_04 ke andar hai
echo - Lekin chahiye parent directory mein
echo.

echo Solution: Parent directory mein naya git repo banayenge
echo.

echo Step 1: F:\hackthone_todo_vibecode mein ja rahe hain...
cd /d F:\hackthone_todo_vibecode

echo.
echo Step 2: Git initialize kar rahe hain...
git init

echo.
echo Step 3: Remote add kar rahe hain...
git remote add origin https://github.com/AsfaQasim/Hackthone_todoapp_vibecode.git

echo.
echo Step 4: Remote check kar rahe hain...
git remote -v

echo.
echo Step 5: .gitignore file check/create...
if not exist .gitignore (
    echo Creating .gitignore...
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
    ) > .gitignore
)

echo.
echo Step 6: Sab files add kar rahe hain...
git add -A

echo.
echo Step 7: Initial commit...
git commit -m "feat: Add complete project with phase_01, phase_02, phase_03, and phase_04

- phase_01: Initial phase
- phase_02: Authentication implementation
- phase_03: Task management features
- phase_04: Docker setup for frontend and backend"

echo.
echo Step 8: Main branch set kar rahe hain...
git branch -M main

echo.
echo Step 9: Remote se pull kar rahe hain (agar kuch hai to)...
git pull origin main --allow-unrelated-histories

echo.
echo Step 10: Push kar rahe hain...
git push -u origin main

echo.
echo ========================================
echo Done! Check GitHub repository
echo ========================================
echo.
pause
