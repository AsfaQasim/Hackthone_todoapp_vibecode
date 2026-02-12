@echo off
echo ========================================
echo Fixing Secrets Issue for GitHub Push
echo ========================================
echo.

echo Current situation:
echo - GitHub detected OpenAI API key in docker-compose.yml
echo - Secrets have been moved to .env.docker (gitignored)
echo - docker-compose.yml now uses env_file instead
echo.

echo Step 1: Staging the fixed docker-compose.yml...
git add docker-compose.yml
git add .gitignore

echo.
echo Step 2: Committing the fix...
git commit -m "fix: Remove hardcoded secrets from docker-compose.yml

- Move all secrets to .env.docker file
- Use env_file in docker-compose.yml
- .env.docker is gitignored for security
- Fixes GitHub secret scanning violation"

echo.
echo Step 3: Attempting to push...
git push origin main

echo.
echo ========================================
echo If push still fails, you have 2 options:
echo ========================================
echo.
echo Option 1: Allow the secret on GitHub (Quick)
echo   Visit: https://github.com/AsfaQasim/Hackthone_todoapp_vibecode/security/secret-scanning/unblock-secret/39XGRYRltwX0ix22zVPwlUY5DN1
echo   Click "Allow secret" button
echo   Then run: git push origin main
echo.
echo Option 2: Rewrite git history (Clean but complex)
echo   This removes the secret from all commits
echo   Run: git filter-branch or use BFG Repo Cleaner
echo.
pause
