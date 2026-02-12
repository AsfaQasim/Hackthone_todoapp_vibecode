# AI Chatbot - Docker Deployment

Complete Docker setup for the AI Chatbot application with FastAPI backend and Next.js frontend.

## 📋 Overview

This repository includes:
- **Backend**: FastAPI application with OpenAI integration
- **Frontend**: Next.js application with modern UI
- **Docker**: Multi-stage builds for optimized images
- **Docker Compose**: Orchestration for easy deployment

## 🚀 Quick Start

### Prerequisites

- Docker Desktop installed and running
- 4GB+ RAM available
- 10GB+ disk space

### 1. Clone and Configure

```bash
# Copy environment template
copy .env.docker.example .env.docker

# Edit with your values
notepad .env.docker
```

### 2. Build Images

```bash
# Windows
docker-build.bat

# Or manually
docker-compose build
```

### 3. Run Application

```bash
# Windows
docker-run.bat

# Or manually
docker-compose up -d
```

### 4. Access Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 📦 Docker Images

### Backend Image
- **Base**: Python 3.11 slim
- **Size**: ~200MB
- **Port**: 8000
- **Health Check**: `/health` endpoint

### Frontend Image
- **Base**: Node 20 Alpine
- **Size**: ~150MB
- **Port**: 3000
- **Multi-stage**: Dependencies → Builder → Runner

## 🛠️ Available Scripts

### Windows Batch Scripts

```bash
docker-build.bat    # Build both images
docker-run.bat      # Start application
docker-stop.bat     # Stop application
```

### Docker Compose Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Restart services
docker-compose restart

# Rebuild and start
docker-compose up -d --build
```

## 🔧 Configuration

### Environment Variables

Required in `.env.docker`:

```env
# Database
DATABASE_URL=postgresql://user:pass@host:5432/db

# Authentication
BETTER_AUTH_SECRET=your-secret-key
JWT_SECRET=your-jwt-secret

# OpenAI
OPENAI_API_KEY=sk-...

# Environment
ENVIRONMENT=production
DEBUG=false
```

### Port Configuration

Default ports in `docker-compose.yml`:
- Frontend: `3000:3000`
- Backend: `8000:8000`

To change ports:

```yaml
services:
  frontend:
    ports:
      - "3001:3000"  # Host:Container
  backend:
    ports:
      - "8001:8000"
```

## 📊 Monitoring

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Last 100 lines
docker-compose logs --tail=100
```

### Container Stats

```bash
# Real-time stats
docker stats

# Specific containers
docker stats ai-chatbot-backend ai-chatbot-frontend
```

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Container health status
docker-compose ps
```

## 🐛 Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs backend

# Check status
docker-compose ps

# Restart
docker-compose restart backend
```

### Port Already in Use

```bash
# Find process
netstat -ano | findstr :8000

# Kill process or change port in docker-compose.yml
```

### Database Connection Failed

```bash
# Check environment variables
docker-compose config

# Test connection
docker-compose exec backend python -c "from src.db import init_db; init_db()"
```

### Clean Rebuild

```bash
# Remove everything
docker-compose down -v --rmi all

# Rebuild
docker-compose build --no-cache
docker-compose up -d
```

## 🚢 Production Deployment

### Build for Production

```bash
# Tag images
docker tag ai-chatbot-backend:latest your-registry/backend:v1.0
docker tag ai-chatbot-frontend:latest your-registry/frontend:v1.0

# Push to registry
docker push your-registry/backend:v1.0
docker push your-registry/frontend:v1.0
```

### Deploy to Cloud

#### Docker Hub

```bash
# Login
docker login

# Push
docker push username/ai-chatbot-backend:latest
docker push username/ai-chatbot-frontend:latest
```

#### AWS ECR

```bash
# Login
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin account.dkr.ecr.us-east-1.amazonaws.com

# Tag
docker tag ai-chatbot-backend:latest account.dkr.ecr.us-east-1.amazonaws.com/backend:latest

# Push
docker push account.dkr.ecr.us-east-1.amazonaws.com/backend:latest
```

#### Google Container Registry

```bash
# Configure
gcloud auth configure-docker

# Tag
docker tag ai-chatbot-backend:latest gcr.io/project-id/backend:latest

# Push
docker push gcr.io/project-id/backend:latest
```

## 🔒 Security

### Best Practices

1. **Never commit secrets** - Use `.env.docker` (gitignored)
2. **Use strong secrets** - Generate random keys
3. **Update regularly** - Keep base images updated
4. **Scan images** - Use `docker scan` or Trivy
5. **Run as non-root** - Already configured in frontend

### Generate Secrets

```bash
# PowerShell
[Convert]::ToBase64String((1..32 | ForEach-Object { Get-Random -Maximum 256 }))

# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## 📈 Performance

### Image Sizes

- Backend: ~200MB (optimized from ~1GB)
- Frontend: ~150MB (optimized from ~800MB)

### Resource Limits

Add to `docker-compose.yml`:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
```

### Build Cache

```bash
# Enable BuildKit
set DOCKER_BUILDKIT=1

# Build with cache
docker-compose build
```

## 🔄 Updates

### Update Application

```bash
# Pull latest code
git pull

# Rebuild images
docker-compose build

# Restart services
docker-compose up -d
```

### Update Dependencies

```bash
# Backend
cd backend
pip freeze > requirements.txt

# Frontend
cd frontend
npm update

# Rebuild
docker-compose build --no-cache
```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Reference](https://docs.docker.com/compose/)
- [FastAPI Docker Guide](https://fastapi.tiangolo.com/deployment/docker/)
- [Next.js Docker Guide](https://nextjs.org/docs/deployment#docker-image)

## 🆘 Support

For issues:
1. Check logs: `docker-compose logs -f`
2. Review health: `docker-compose ps`
3. Inspect container: `docker inspect <container>`
4. Check documentation: `DOCKER_SETUP.md`

## 📝 License

See main repository LICENSE file.
