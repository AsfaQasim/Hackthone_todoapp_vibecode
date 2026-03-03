@echo off
echo ========================================
echo Fixing Route 404 Errors
echo ========================================
echo.

echo Step 1: Stopping any running dev server...
taskkill /F /IM node.exe 2>nul
timeout /t 2 /nobreak >nul

echo Step 2: Deleting .next folder...
if exist .next (
    rmdir /s /q .next
    echo .next folder deleted
) else (
    echo .next folder not found
)


echo Step 3: Deleting node_modules/.cache...
if exist node_modules\.cache (
    rmdir /s /q node_modules\.cache
    echo Cache deleted
)

echo Step 4: Installing missing packages...
call npm install

echo.
echo ========================================
echo Fix Complete! Now starting dev server...
echo ========================================
echo.

call npm run dev
