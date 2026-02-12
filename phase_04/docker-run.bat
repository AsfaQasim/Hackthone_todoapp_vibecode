@echo off
REM Docker Run Script for AI Chatbot Application
REM This script starts the application using Docker Compose

echo ========================================
echo Starting AI Chatbot Application
echo ========================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not running!
    echo Please start Docker Desktop and try again.
    pause
    exit /b 1
)

REM Check if .env.docker exists
if not exist .env.docker (
    echo WARNING: .env.docker file not found!
    echo Creating from example...
    if exist .env.docker.example (
        copy .env.docker.example .env.docker
        echo.
        echo Please edit .env.docker with your configuration
        echo Then run this script again.
        pause
        exit /b 1
    ) else (
        echo ERROR: .env.docker.example not found!
        pause
        exit /b 1
    )
)

echo Starting services with Docker Compose...
echo.

docker-compose --env-file .env.docker up -d

if errorlevel 1 (
    echo ERROR: Failed to start services!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Application Started Successfully!
echo ========================================
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo To view logs:
echo   docker-compose logs -f
echo.
echo To stop:
echo   docker-compose down
echo.

REM Wait a moment then show logs
timeout /t 3 /nobreak >nul
echo Showing logs (Press Ctrl+C to exit)...
echo.
docker-compose logs -f

pause
