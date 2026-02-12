@echo off
REM Docker Prerequisites Check Script

echo ========================================
echo Docker Prerequisites Check
echo ========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if errorlevel 1 (
    echo [X] Docker is NOT installed
    echo     Please install Docker Desktop from https://www.docker.com/products/docker-desktop
    set DOCKER_OK=0
) else (
    echo [✓] Docker is installed
    docker --version
    set DOCKER_OK=1
)
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo [X] Docker is NOT running
    echo     Please start Docker Desktop
    set DOCKER_RUNNING=0
) else (
    echo [✓] Docker is running
    set DOCKER_RUNNING=1
)
echo.

REM Check Docker Compose
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo [X] Docker Compose is NOT installed
    set COMPOSE_OK=0
) else (
    echo [✓] Docker Compose is installed
    docker-compose --version
    set COMPOSE_OK=1
)
echo.

REM Check .env.docker file
if exist .env.docker (
    echo [✓] .env.docker file exists
    set ENV_OK=1
) else (
    echo [X] .env.docker file NOT found
    echo     Run: copy .env.docker.example .env.docker
    set ENV_OK=0
)
echo.

REM Check Dockerfile existence
if exist backend\Dockerfile (
    echo [✓] Backend Dockerfile exists
    set BACKEND_DOCKERFILE=1
) else (
    echo [X] Backend Dockerfile NOT found
    set BACKEND_DOCKERFILE=0
)

if exist frontend\Dockerfile (
    echo [✓] Frontend Dockerfile exists
    set FRONTEND_DOCKERFILE=1
) else (
    echo [X] Frontend Dockerfile NOT found
    set FRONTEND_DOCKERFILE=0
)
echo.

REM Check docker-compose.yml
if exist docker-compose.yml (
    echo [✓] docker-compose.yml exists
    set COMPOSE_FILE=1
) else (
    echo [X] docker-compose.yml NOT found
    set COMPOSE_FILE=0
)
echo.

REM Summary
echo ========================================
echo Summary
echo ========================================

if %DOCKER_OK%==1 if %DOCKER_RUNNING%==1 if %COMPOSE_OK%==1 if %ENV_OK%==1 if %BACKEND_DOCKERFILE%==1 if %FRONTEND_DOCKERFILE%==1 if %COMPOSE_FILE%==1 (
    echo.
    echo [✓] All prerequisites met!
    echo     You can now run: docker-build.bat
    echo.
) else (
    echo.
    echo [X] Some prerequisites are missing
    echo     Please fix the issues above
    echo.
)

pause
