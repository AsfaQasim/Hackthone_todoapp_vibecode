@echo off
echo ========================================
echo CLEARING PYTHON CACHE
echo ========================================
echo.
echo Deleting all __pycache__ folders...
cd backend
for /d /r %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d" && echo Deleted: %%d
echo.
echo Deleting all .pyc files...
del /s /q *.pyc 2>nul
echo.
echo ✅ Python cache cleared!
echo.
echo Now restart backend:
echo   cd backend
echo   python -m uvicorn main:app --reload
echo.
pause
