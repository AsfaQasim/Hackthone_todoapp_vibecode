@echo off
echo ========================================
echo STARTING BACKEND WITH FIXES
echo ========================================
echo.
cd backend
echo Starting backend server...
python -m uvicorn main:app --reload
