@echo off
echo ========================================
echo Force Push with Clean History
echo ========================================
echo.
echo WARNING: Ye git history rewrite karega!
echo Backup zaroor le lo pehle.
echo.
echo Kya aap repository ke admin/owner ho? (Y/N)
set /p IS_ADMIN="Answer: "
echo.

if /i "%IS_ADMIN%"=="N" (
    echo.
    echo Aapko repository admin se help chahiye!
    echo.
    echo Admin se ye kaho:
    echo 1. Settings -^> Branches -^> main branch protection disable karo
    echo 2. Mujhe force push karne do
    echo 3. Phir wapas enable kar do
    echo.
    pause
    exit
)

echo Step 1: Main branch pe jao...
git checkout main
echo.

echo Step 2: Sensitive files remove karo...
git rm --cached backend/.env 2>nul
git rm --cached frontend/.env 2>nul
git rm --cached .env 2>nul
git rm --cached .env.local 2>nul
git rm --cached .env.docker 2>nul
git rm --cached frontend/.env.local 2>nul
git rm --cached frontend/.env.production 2>nul
git rm -r --cached __pycache__ 2>nul
git rm -r --cached backend/__pycache__ 2>nul
git rm -r --cached .pytest_cache 2>nul
echo.

echo Step 3: .gitignore add karo...
git add .gitignore .env.example frontend/.env.example
echo.

echo Step 4: Commit karo...
git commit -m "chore: Remove secrets and add .gitignore"
echo.

echo Step 5: Force push (branch protection disable hona chahiye)...
git push origin main --force
echo.

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ❌ Push fail ho gaya!
    echo.
    echo Possible reasons:
    echo 1. Branch protection abhi bhi enabled hai
    echo 2. Admin rights nahi hain
    echo.
    echo Solution:
    echo - GitHub Settings -^> Branches -^> Disable protection
    echo - Ya admin se help lo
    echo.
) else (
    echo.
    echo ✅ Successfully pushed!
    echo.
    echo Ab branch protection wapas enable kar do:
    echo Settings -^> Branches -^> Enable protection rules
    echo.
)

pause
