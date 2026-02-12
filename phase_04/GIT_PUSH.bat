@echo off
echo ========================================
echo Git Push with Secrets Removed
echo ========================================
echo.

echo Step 1: Adding .gitignore and example files...
git add .gitignore .env.example frontend/.env.example SECRETS_REMOVED.md
echo.

echo Step 2: Removing cached .env files...
git rm --cached backend/.env frontend/.env .env .env.local .env.docker frontend/.env.local frontend/.env.production 2>nul
git rm --cached __pycache__/*.pyc 2>nul
git rm --cached backend/__pycache__/*.pyc 2>nul
git rm --cached frontend/.next/* 2>nul
echo.

echo Step 3: Adding all other changes...
git add .
echo.

echo Step 4: Committing...
git commit -m "fix: Remove secrets and add .gitignore

- Added .gitignore to exclude sensitive files
- Created .env.example files for documentation
- Removed real secrets from repository
- Added SECRETS_REMOVED.md with instructions
- Fixed Docker deployment issues
- Fixed auth middleware for tasks endpoints
- Fixed general-task-execution page routing"
echo.

echo Step 5: Pushing to GitHub...
git push origin main
echo.

echo ========================================
echo Done!
echo ========================================
echo.
echo If push still fails due to branch protection:
echo 1. Create a new branch: git checkout -b fix/remove-secrets
echo 2. Push branch: git push origin fix/remove-secrets
echo 3. Create Pull Request on GitHub
echo.
pause
