@echo off
echo ========================================
echo Clean Secrets from Git History
echo ========================================
echo.
echo WARNING: This will rewrite git history!
echo Make sure you have a backup.
echo.
pause

echo Step 1: Going back to main branch...
git checkout main
echo.

echo Step 2: Deleting the problematic branch...
git branch -D fix/remove-secrets-and-fixes 2>nul
echo.

echo Step 3: Removing sensitive files completely...
git rm --cached backend/.env 2>nul
git rm --cached frontend/.env 2>nul
git rm --cached .env 2>nul
git rm --cached .env.local 2>nul
git rm --cached .env.docker 2>nul
git rm --cached frontend/.env.local 2>nul
git rm --cached frontend/.env.production 2>nul
git rm --cached backend/.env.example 2>nul
git rm -r --cached __pycache__ 2>nul
git rm -r --cached backend/__pycache__ 2>nul
git rm -r --cached frontend/.next 2>nul
git rm -r --cached .pytest_cache 2>nul
echo.

echo Step 4: Adding .gitignore...
git add .gitignore
echo.

echo Step 5: Committing removal...
git commit -m "chore: Remove sensitive files from tracking"
echo.

echo Step 6: Force push to main (if you have permission)...
echo If this fails, you need to:
echo 1. Contact repo admin to temporarily disable branch protection
echo 2. Or create a new repository
echo.
git push origin main --force
echo.

echo ========================================
echo Alternative Solution
echo ========================================
echo.
echo If force push fails, you have 2 options:
echo.
echo Option 1: Create New Repository
echo   1. Create new repo on GitHub
echo   2. git remote set-url origin NEW_REPO_URL
echo   3. git push -u origin main
echo.
echo Option 2: Contact Admin
echo   Ask repository admin to:
echo   1. Temporarily disable branch protection
echo   2. Allow force push
echo   3. Then run: git push origin main --force
echo.
pause
