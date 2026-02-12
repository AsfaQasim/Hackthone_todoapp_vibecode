@echo off
echo ========================================
echo Remove Secrets from Git History
echo ========================================
echo.
echo Ye script git history se secrets remove karega
echo.
pause

echo Step 1: Installing git-filter-repo...
pip install git-filter-repo
echo.

echo Step 2: Backup banao (important!)...
cd ..
xcopy phase_04 phase_04_backup /E /I /H /Y
cd phase_04
echo Backup created: phase_04_backup
echo.

echo Step 3: Remove .env files from entire history...
git filter-repo --path backend/.env --invert-paths --force
git filter-repo --path frontend/.env --invert-paths --force
git filter-repo --path .env --invert-paths --force
git filter-repo --path .env.local --invert-paths --force
git filter-repo --path .env.docker --invert-paths --force
git filter-repo --path frontend/.env.local --invert-paths --force
git filter-repo --path frontend/.env.production --invert-paths --force
echo.

echo Step 4: Remove __pycache__ from history...
git filter-repo --path __pycache__ --invert-paths --force
git filter-repo --path backend/__pycache__ --invert-paths --force
git filter-repo --path .pytest_cache --invert-paths --force
echo.

echo Step 5: Re-add remote...
git remote add origin https://github.com/AsfaQasim/Hackthone_todoapp_vibecode.git
echo.

echo Step 6: Force push...
git push origin main --force
echo.

echo ========================================
echo Done!
echo ========================================
echo.
echo Agar error aaye to:
echo 1. Check if git-filter-repo installed: pip show git-filter-repo
echo 2. Backup se restore karo: xcopy ..\phase_04_backup phase_04 /E /I /H /Y
echo.
pause
