@echo off
cls
echo ========================================
echo STARTING BACKEND - CLEAN
echo ========================================
echo.
cd backend
echo Starting uvicorn...
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
