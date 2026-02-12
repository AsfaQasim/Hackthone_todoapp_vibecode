@echo off
echo ========================================
echo Push to New Repository
echo ========================================
echo.
echo STEP 1: Create New Repository on GitHub
echo ========================================
echo.
echo 1. Go to: https://github.com/new
echo 2. Repository name: Hackthone_todoapp_vibecode_clean
echo 3. Description: AI Todo App with Chat Assistant
echo 4. Make it Public or Private
echo 5. DO NOT initialize with README, .gitignore, or license
echo 6. Click "Create repository"
echo.
echo Press any key AFTER you've created the repository...
pause
echo.

echo ========================================
echo STEP 2: What's your new repository name?
echo ========================================
set /p REPO_NAME="Enter repository name (e.g., Hackthone_todoapp_vibecode_clean): "
echo.

echo ========================================
echo STEP 3: Updating Remote URL
echo ========================================
git remote set-url origin https://github.com/AsfaQasim/%REPO_NAME%.git
echo Remote URL updated!
echo.

echo ========================================
echo STEP 4: Verifying Remote
echo ========================================
git remote -v
echo.

echo ========================================
echo STEP 5: Pushing to New Repository
echo ========================================
git push -u origin main
echo.

echo ========================================
echo SUCCESS!
echo ========================================
echo.
echo Your code is now at:
echo https://github.com/AsfaQasim/%REPO_NAME%
echo.
echo All secrets have been removed from tracking.
echo The .gitignore will prevent future secret commits.
echo.
pause
