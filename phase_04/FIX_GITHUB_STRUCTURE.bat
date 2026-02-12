@echo off
echo ========================================
echo GitHub Structure Fix - phase_04 Folder Banana
echo ========================================
echo.

echo Aap abhi phase_04 folder mein ho
echo GitHub par ye files root mein push ho gayi hain
echo.
echo Fix: Parent directory se push karna padega
echo.

echo Step 1: Parent directory mein ja rahe hain...
cd ..

echo.
echo Step 2: Current location check...
echo %CD%
echo.

echo Step 3: Git status check...
git status

echo.
echo Step 4: Agar changes hain to commit karenge...
git add -A
git commit -m "fix: Organize repository with phase_04 folder structure"

echo.
echo Step 5: Push kar rahe hain...
git push origin main

echo.
echo ========================================
echo Done! GitHub structure should be correct now
echo ========================================
echo.
echo Expected structure on GitHub:
echo - phase_01/
echo - phase_02/
echo - phase_03/
echo - phase_04/
echo.
pause
