@echo off
echo ========================================
echo Git Repository Dhundh Rahe Hain
echo ========================================
echo.

echo Checking F:\hackthone_todo_vibecode\phase_04
if exist "F:\hackthone_todo_vibecode\phase_04\.git" (
    echo FOUND: Git repo in F:\hackthone_todo_vibecode\phase_04
    echo.
    cd /d F:\hackthone_todo_vibecode\phase_04
    git remote -v
) else (
    echo NOT FOUND in phase_04
)

echo.
echo Checking F:\hackthone_todo_vibecode
if exist "F:\hackthone_todo_vibecode\.git" (
    echo FOUND: Git repo in F:\hackthone_todo_vibecode
    echo.
    cd /d F:\hackthone_todo_vibecode
    git remote -v
) else (
    echo NOT FOUND in hackthone_todo_vibecode
)

echo.
echo Checking F:\phase_04
if exist "F:\phase_04\.git" (
    echo FOUND: Git repo in F:\phase_04
    echo.
    cd /d F:\phase_04
    git remote -v
) else (
    echo NOT FOUND in F:\phase_04
)

echo.
echo ========================================
pause
