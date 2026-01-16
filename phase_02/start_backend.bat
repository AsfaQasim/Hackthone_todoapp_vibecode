#!/bin/bash
# Script to start the backend server

echo "Starting the backend server..."

# Change to the backend directory
cd F:\hackthone_todo_vibecode\phase_02\backend

# Install dependencies if not already installed
pip install -r requirements.txt

# Run the server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000