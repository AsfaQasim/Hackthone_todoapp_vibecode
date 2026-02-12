@echo off
echo ========================================
echo Fixing Folder Structure - phase_04 Folder Banana
echo ========================================
echo.

echo Current location: %CD%
echo.

echo Step 1: Parent directory mein ja rahe hain...
cd ..
echo Now in: %CD%
echo.

echo Step 2: Git pull kar rahe hain...
git pull origin main

echo.
echo Step 3: phase_04 folder check kar rahe hain...
if exist phase_04 (
    echo phase_04 folder already exists
) else (
    echo phase_04 folder nahi hai, structure galat hai
    echo.
    echo Fixing structure...
    
    REM Create phase_04 folder
    mkdir phase_04_temp
    
    REM Move everything except phase folders to phase_04_temp
    echo Moving files to phase_04_temp...
    for %%F in (*) do (
        if not "%%F"=="phase_01" if not "%%F"=="phase_02" if not "%%F"=="phase_03" if not "%%F"=="phase_04_temp" if not "%%F"==".git" (
            move "%%F" phase_04_temp\
        )
    )
    
    REM Rename to phase_04
    move phase_04_temp phase_04
    
    echo.
    echo Step 4: Git add kar rahe hain...
    git add -A
    
    echo.
    echo Step 5: Commit kar rahe hain...
    git commit -m "fix: Move all files to phase_04 folder to match project structure"
    
    echo.
    echo Step 6: Push kar rahe hain...
    git push origin main
)

echo.
echo ========================================
echo Done! Check GitHub repository structure
echo ========================================
echo.
pause
