@echo off
echo ========================================
echo STARTING BACKEND FRESH
echo ========================================
echo.
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
