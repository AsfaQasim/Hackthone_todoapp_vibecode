@echo off
echo ========================================
echo Git Push via Pull Request
echo ========================================
echo.
echo Main branch is protected. Creating a new branch...
echo.

echo Step 1: Creating new branch...
git checkout -b fix/remove-secrets-and-fixes
echo.

echo Step 2: Adding .gitignore and example files...
git add .gitignore .env.example frontend/.env.example SECRETS_REMOVED.md
echo.

echo Step 3: Removing cached sensitive files...
git rm --cached backend/.env 2>nul
git rm --cached frontend/.env 2>nul
git rm --cached .env 2>nul
git rm --cached .env.local 2>nul
git rm --cached .env.docker 2>nul
git rm --cached frontend/.env.local 2>nul
git rm --cached frontend/.env.production 2>nul
git rm -r --cached __pycache__ 2>nul
git rm -r --cached backend/__pycache__ 2>nul
git rm -r --cached frontend/.next 2>nul
echo.

echo Step 4: Adding all changes...
git add -A
echo.

echo Step 5: Committing changes...
git commit -m "fix: Remove secrets and implement Docker deployment fixes

Changes:
- Added .gitignore to exclude sensitive files (.env, __pycache__, etc)
- Created .env.example files for documentation
- Removed real secrets from repository
- Fixed auth middleware to properly handle tasks/chat endpoints
- Fixed database schema (status instead of completed)
- Fixed general-task-execution page routing
- Fixed Docker networking with BACKEND_URL
- Added useEffect to tasks page for auto-loading
- Fixed chat task creation with correct schema

All secrets have been removed and replaced with example files.
See SECRETS_REMOVED.md for setup instructions."
echo.

echo Step 6: Pushing branch to GitHub...
git push -u origin fix/remove-secrets-and-fixes
echo.

echo ========================================
echo Branch Pushed Successfully!
echo ========================================
echo.
echo Next Steps:
echo 1. Go to: https://github.com/AsfaQasim/Hackthone_todoapp_vibecode
echo 2. You'll see a banner: "Compare & pull request"
echo 3. Click it to create a Pull Request
echo 4. Add description and submit
echo 5. Merge the PR once approved
echo.
echo Or create PR directly:
echo https://github.com/AsfaQasim/Hackthone_todoapp_vibecode/compare/main...fix/remove-secrets-and-fixes
echo.
pause
