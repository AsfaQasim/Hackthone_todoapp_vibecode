# Docker Setup Guide

This guide explains how to build and run the AI Chatbot application using Docker.

## Prerequisites

- Docker Engine 20.10+ installed
- Docker Compose 2.0+ installed
- At least 4GB of available RAM
- 10GB of free disk space

## Quick Start

### 1. Environment Configuration

Create a `.env.docker` file in the root directory:

```bash
cp .env.docker.example .env.docker
```

Edit `.env.docker` and add your configuration:

```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
BETTER_AUTH_SECRET=your-secret-key
JWT_SECRET=your-jwt-secret
OPENAI_API_KEY=your-openai-key
```

### 2. Build Images

Build both frontend and backend images:

```bash
# Build all services
docker-compose build

# Or build individually
docker-compose build backend
docker-compose build frontend
```

### 3. Run Containers

Start all services:

```bash
docker-compose up -d
```

Check logs:

```bash
docker-compose logs -f
```

### 4. Access Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Individual Service Commands

### Backend Only

```bash
# Build backend image
docker build -t ai-chatbot-backend ./backend

# Run backend container
docker run -d \
  --name backend \
  -p 8000:8000 \
  --env-file backend/.env \
  ai-chatbot-backend

# View logs
docker logs -f backend
```

### Frontend Only

```bash
# Build frontend image
docker build -t ai-chatbot-frontend ./frontend

# Run frontend container
docker run -d \
  --name frontend \
  -p 3000:3000 \
  --env-file frontend/.env.local \
  ai-chatbot-frontend

# View logs
docker logs -f frontend
```

## Docker Compose Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart services
docker-compose restart

# View logs
docker-compose logs -f [service_name]

# Rebuild and restart
docker-compose up -d --build

# Remove all containers and volumes
docker-compose down -v
```

## Image Management

### Build Images

```bash
# Build with tag
docker build -t ai-chatbot-backend:v1.0 ./backend
docker build -t ai-chatbot-frontend:v1.0 ./frontend
```

### Push to Registry

```bash
# Tag for registry
docker tag ai-chatbot-backend:v1.0 your-registry/ai-chatbot-backend:v1.0
docker tag ai-chatbot-frontend:v1.0 your-registry/ai-chatbot-frontend:v1.0

# Push to registry
docker push your-registry/ai-chatbot-backend:v1.0
docker push your-registry/ai-chatbot-frontend:v1.0
```

### Pull from Registry

```bash
docker pull your-registry/ai-chatbot-backend:v1.0
docker pull your-registry/ai-chatbot-frontend:v1.0
```

## Production Deployment

### Using Docker Compose

1. Update `.env.docker` with production values
2. Set `ENVIRONMENT=production` and `DEBUG=false`
3. Use production database URL
4. Deploy:

```bash
docker-compose -f docker-compose.yml up -d
```

### Using Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Deploy stack
docker stack deploy -c docker-compose.yml ai-chatbot

# Check services
docker service ls

# Scale services
docker service scale ai-chatbot_backend=3
docker service scale ai-chatbot_frontend=2
```

### Using Kubernetes

Convert docker-compose to Kubernetes manifests:

```bash
# Install kompose
curl -L https://github.com/kubernetes/kompose/releases/download/v1.31.2/kompose-windows-amd64.exe -o kompose.exe

# Convert
kompose convert -f docker-compose.yml

# Deploy
kubectl apply -f .
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Check container status
docker-compose ps

# Restart specific service
docker-compose restart backend
```

### Database Connection Issues

```bash
# Test database connection from backend
docker-compose exec backend python -c "from src.db import init_db; init_db()"
```

### Port Already in Use

```bash
# Find process using port
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# Kill process or change port in docker-compose.yml
```

### Clean Rebuild

```bash
# Remove all containers, images, and volumes
docker-compose down -v --rmi all

# Rebuild from scratch
docker-compose build --no-cache
docker-compose up -d
```

## Health Checks

Both services include health checks:

```bash
# Check backend health
curl http://localhost:8000/health

# Check frontend health (if implemented)
curl http://localhost:3000/api/health

# Docker health status
docker-compose ps
```

## Performance Optimization

### Multi-stage Builds

Both Dockerfiles use multi-stage builds to minimize image size:

- Backend: ~200MB (vs ~1GB without optimization)
- Frontend: ~150MB (vs ~800MB without optimization)

### Build Cache

Use BuildKit for faster builds:

```bash
# Enable BuildKit
set DOCKER_BUILDKIT=1

# Build with cache
docker-compose build
```

### Resource Limits

Add resource limits in docker-compose.yml:

```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
        reservations:
          cpus: '0.5'
          memory: 512M
```

## Security Best Practices

1. **Never commit .env files** - Use .env.example templates
2. **Use secrets management** - Docker secrets or external vaults
3. **Run as non-root** - Frontend already uses non-root user
4. **Scan images** - Use `docker scan` or Trivy
5. **Update base images** - Regularly update Python and Node versions
6. **Limit network exposure** - Use internal networks where possible

## Monitoring

### Container Stats

```bash
# Real-time stats
docker stats

# Specific container
docker stats backend frontend
```

### Logs

```bash
# Follow logs
docker-compose logs -f

# Last 100 lines
docker-compose logs --tail=100

# Specific service
docker-compose logs -f backend
```

## Backup and Restore

### Backup Data

```bash
# Backup volumes
docker run --rm -v backend-data:/data -v $(pwd):/backup alpine tar czf /backup/backend-data.tar.gz /data
```

### Restore Data

```bash
# Restore volumes
docker run --rm -v backend-data:/data -v $(pwd):/backup alpine tar xzf /backup/backend-data.tar.gz -C /
```

## Support

For issues or questions:
- Check logs: `docker-compose logs -f`
- Review health checks: `docker-compose ps`
- Inspect containers: `docker inspect <container_name>`
