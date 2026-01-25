@echo off
REM Script to start the backend server

echo Starting the backend server...

REM Change to the backend directory
cd /d "F:\hackthone_todo_vibecode\phase_02\backend"

REM Install dependencies if not already installed
pip install -r requirements.txt

REM Add the backend directory to the Python path to ensure modules can be imported correctly
set PYTHONPATH=%cd%

REM Run the server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000