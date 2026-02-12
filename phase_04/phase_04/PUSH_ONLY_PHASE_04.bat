@echo off
echo ========================================
echo Sirf Phase_04 Ko Push Karna
echo ========================================
echo.

echo Step 1: phase_04 directory mein ja rahe hain...
cd /d F:\hackthone_todo_vibecode\phase_04

echo.
echo Step 2: Git initialize kar rahe hain...
git init

echo.
echo Step 3: Remote add kar rahe hain...
git remote add origin https://github.com/AsfaQasim/Hackthone_todoapp_vibecode.git

echo.
echo Step 4: .gitignore check kar rahe hain...
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
        echo backend/__pycache__/
        echo frontend/.next/
        echo frontend/node_modules/
    ) > .gitignore
)

echo.
echo Step 5: Sab files add kar rahe hain...
git add -A

echo.
echo Step 6: Commit kar rahe hain...
git commit -m "feat: Phase 04 - Docker setup for AI Chatbot with Frontend and Backend

- Backend: FastAPI with Docker
- Frontend: Next.js with Docker
- Docker Compose for orchestration
- Environment variables in .env.docker (gitignored)
- Multi-stage builds for optimization"

echo.
echo Step 7: Main branch set kar rahe hain...
git branch -M main

echo.
echo Step 8: Push kar rahe hain...
git push -u origin main --force

echo.
echo ========================================
echo Done! Phase_04 pushed to GitHub root
echo ========================================
echo.
echo GitHub URL: https://github.com/AsfaQasim/Hackthone_todoapp_vibecode
echo.
echo Structure on GitHub (root level):
echo - backend/
echo - frontend/
echo - docker-compose.yml
echo - README.md
echo - etc.
echo.
pause
