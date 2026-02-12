@echo off
echo ========================================
echo Removing Secrets from Git History
echo ========================================
echo.

echo Step 1: Creating backup branch...
git branch backup-before-secret-removal
echo Backup created: backup-before-secret-removal
echo.

echo Step 2: Removing secrets from git history...
echo This will rewrite git history to remove the OpenAI API key
echo.

git filter-branch --force --index-filter "git rm --cached --ignore-unmatch docker-compose.yml" --prune-empty --tag-name-filter cat -- --all

echo.
echo Step 3: Adding cleaned docker-compose.yml...
git add docker-compose.yml
git commit -m "fix: Remove hardcoded secrets from docker-compose.yml, use .env.docker instead"

echo.
echo Step 4: Force pushing to remote...
echo WARNING: This will rewrite remote history!
echo.
pause

git push origin main --force

echo.
echo ========================================
echo Done! Secrets removed from git history
echo ========================================
echo.
echo Your .env.docker file (which is gitignored) still has the secrets
echo Docker containers will work normally using .env.docker
echo.
pause
