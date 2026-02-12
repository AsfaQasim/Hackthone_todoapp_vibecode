@echo off
echo ========================================
echo Phase_04 Ko Sahi Tarike Se Push Karna
echo ========================================
echo.

echo Step 1: Sahi directory mein ja rahe hain...
cd /d F:\hackthone_todo_vibecode

echo.
echo Step 2: Current location:
cd
echo.

echo Step 3: Folders check kar rahe hain...
dir /b | findstr phase

echo.
echo Step 4: Git status check...
git status

echo.
echo Step 5: Sab files add kar rahe hain...
git add -A

echo.
echo Step 6: Commit kar rahe hain...
git commit -m "feat: Add phase_04 with Docker setup for frontend and backend"

echo.
echo Step 7: Push kar rahe hain...
git push origin main

echo.
echo ========================================
echo Done! Phase_04 pushed to GitHub
echo ========================================
echo.
echo GitHub structure:
echo https://github.com/AsfaQasim/Hackthone_todoapp_vibecode
echo.
echo Expected folders:
echo - phase_01/
echo - phase_02/
echo - phase_03/
echo - phase_04/  (NEW)
echo.
pause
