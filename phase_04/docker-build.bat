@echo off
REM Docker Build Script for AI Chatbot Application
REM This script builds Docker images for both frontend and backend

echo ========================================
echo Building AI Chatbot Docker Images
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

echo Docker is running...
echo.

REM Build Backend
echo ========================================
echo Building Backend Image...
echo ========================================
cd backend
docker build -t ai-chatbot-backend:latest .
if errorlevel 1 (
    echo ERROR: Backend build failed!
    cd ..
    pause
    exit /b 1
)
cd ..
echo Backend image built successfully!
echo.

REM Build Frontend
echo ========================================
echo Building Frontend Image...
echo ========================================
cd frontend
docker build -t ai-chatbot-frontend:latest .
if errorlevel 1 (
    echo ERROR: Frontend build failed!
    cd ..
    pause
    exit /b 1
)
cd ..
echo Frontend image built successfully!
echo.

REM List images
echo ========================================
echo Docker Images:
echo ========================================
docker images | findstr ai-chatbot
echo.

echo ========================================
echo Build Complete!
echo ========================================
echo.
echo To run the application:
echo   docker-compose up -d
echo.
echo To view logs:
echo   docker-compose logs -f
echo.

pause
