@echo off
REM Docker Quick Start Script - Complete Setup and Run

echo ========================================
echo AI Chatbot - Docker Quick Start
echo ========================================
echo.

REM Step 1: Check prerequisites
echo Step 1: Checking prerequisites...
echo.
call docker-check.bat
if errorlevel 1 (
    echo.
    echo Please fix the issues above and run this script again.
    pause
    exit /b 1
)

echo.
echo ========================================
echo.

REM Step 2: Setup environment
echo Step 2: Setting up environment...
echo.
if not exist .env.docker (
    if exist .env.docker.example (
        copy .env.docker.example .env.docker
        echo Created .env.docker from example
        echo.
        echo IMPORTANT: Please edit .env.docker with your configuration:
        echo   - DATABASE_URL
        echo   - BETTER_AUTH_SECRET
        echo   - JWT_SECRET
        echo   - OPENAI_API_KEY
        echo.
        notepad .env.docker
        echo.
        echo Press any key after saving your configuration...
        pause >nul
    )
) else (
    echo .env.docker already exists
)

echo.
echo ========================================
echo.

REM Step 3: Build images
echo Step 3: Building Docker images...
echo This may take several minutes on first run...
echo.
call docker-build.bat
if errorlevel 1 (
    echo.
    echo Build failed! Please check the errors above.
    pause
    exit /b 1
)

echo.
echo ========================================
echo.

REM Step 4: Start application
echo Step 4: Starting application...
echo.
docker-compose --env-file .env.docker up -d

if errorlevel 1 (
    echo.
    echo Failed to start application!
    pause
    exit /b 1
)

echo.
echo ========================================
echo Application Started Successfully!
echo ========================================
echo.
echo Access your application:
echo   Frontend:  http://localhost:3000
echo   Backend:   http://localhost:8000
echo   API Docs:  http://localhost:8000/docs
echo.
echo Useful commands:
echo   View logs:     docker-compose logs -f
echo   Stop app:      docker-compose down
echo   Restart:       docker-compose restart
echo.
echo Opening browser in 5 seconds...
timeout /t 5 /nobreak >nul

REM Open browser
start http://localhost:3000

echo.
echo Press any key to view logs...
pause >nul

docker-compose logs -f
