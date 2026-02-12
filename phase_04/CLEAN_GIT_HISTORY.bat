@echo off
echo ========================================
echo Git History Se Secrets Remove Karna
echo ========================================
echo.

echo Step 1: Backup branch bana rahe hain...
git branch backup-before-clean
echo Backup created: backup-before-clean
echo.

echo Step 2: Git history se docker-compose.yml remove kar rahe hain...
git filter-branch -f --index-filter "git rm --cached --ignore-unmatch docker-compose.yml" --prune-empty -- --all

echo.
echo Step 3: Cleaned docker-compose.yml add kar rahe hain...
git add docker-compose.yml .env.docker.example

echo.
echo Step 4: Naya commit bana rahe hain...
git commit -m "fix: Remove secrets from docker-compose.yml, use .env.docker"

echo.
echo Step 5: Cleanup kar rahe hain...
git reflog expire --expire=now --all
git gc --prune=now --aggressive

echo.
echo Step 6: Force push kar rahe hain...
echo WARNING: Ye git history rewrite karega!
echo.
pause

git push origin main --force

echo.
echo ========================================
echo Done! Git history clean ho gayi!
echo ========================================
echo.
pause
