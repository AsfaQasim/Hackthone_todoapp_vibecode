@echo off
echo ========================================
echo Simple Method: Git History Clean Karna
echo ========================================
echo.

echo Backup bana rahe hain...
git branch backup-original
echo.

echo Method 1: Orphan branch se fresh start
echo ========================================
echo.

REM Create new orphan branch (no history)
git checkout --orphan clean-main

REM Add all current files
git add -A

REM Commit everything fresh
git commit -m "Initial commit: Clean repository without secrets

- Docker setup with .env.docker for secrets
- Frontend and Backend with Dockerfiles
- All secrets moved to .env.docker (gitignored)
- Clean git history"

echo.
echo Purani main branch delete kar rahe hain...
git branch -D main

echo.
echo Naya main branch bana rahe hain...
git branch -m main

echo.
echo Force push kar rahe hain...
echo WARNING: Ye complete git history replace kar dega!
echo.
pause

git push -f origin main

echo.
echo ========================================
echo Done! Git history completely clean!
echo ========================================
echo.
echo Agar kuch galat ho jaye to backup branch hai:
echo git checkout backup-original
echo.
pause
