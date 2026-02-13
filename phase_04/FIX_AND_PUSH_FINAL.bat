@echo off
echo ========================================
echo Final Fix and Push - Clean Structure
echo ========================================
echo.

echo Step 1: Current directory
cd /d F:\hackthone_todo_vibecode
cd
echo.

echo Step 2: Git status check...
git status

echo.
echo Step 3: Sab changes commit kar rahe hain (deletions included)...
git add -A

echo.
echo Step 4: Commit kar rahe hain...
git commit -m "fix: Clean up nested phase folders and establish correct structure

- Remove nested phase_04/phase_03 and phase_04/phase_04
- Keep only root level phase folders
- phase_01, phase_02, phase_03, phase_04 at root level"

echo.
echo Step 5: Push kar rahe hain...
git push origin main

echo.
echo ========================================
echo Done! Check GitHub
echo ========================================
echo.
echo GitHub URL: https://github.com/AsfaQasim/Hackthone_todoapp_vibecode
echo.
pause
