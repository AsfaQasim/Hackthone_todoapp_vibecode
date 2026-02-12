# Docker Build and Push Guide

Complete guide for building Docker images and pushing them to container registries.

## 🏗️ Building Images

### Local Build

#### Using Scripts (Windows)
```bash
# Check prerequisites first
docker-check.bat

# Build both images
docker-build.bat
```

#### Using Docker Compose
```bash
# Build all services
docker-compose build

# Build specific service
docker-compose build backend
docker-compose build frontend

# Build without cache (clean build)
docker-compose build --no-cache
```

#### Using Docker CLI
```bash
# Backend
cd backend
docker build -t ai-chatbot-backend:latest .
cd ..

# Frontend
cd frontend
docker build -t ai-chatbot-frontend:latest .
cd ..
```

### Build with Tags

```bash
# Version tags
docker build -t ai-chatbot-backend:v1.0.0 ./backend
docker build -t ai-chatbot-frontend:v1.0.0 ./frontend

# Multiple tags
docker build -t ai-chatbot-backend:latest -t ai-chatbot-backend:v1.0.0 ./backend
```

### Build Arguments

```bash
# Pass build arguments
docker build --build-arg PYTHON_VERSION=3.11 -t ai-chatbot-backend:latest ./backend
```

## 📤 Pushing to Registries

### Docker Hub

#### Setup
```bash
# Login
docker login

# Enter username and password when prompted
```

#### Tag Images
```bash
# Format: username/repository:tag
docker tag ai-chatbot-backend:latest yourusername/ai-chatbot-backend:latest
docker tag ai-chatbot-backend:latest yourusername/ai-chatbot-backend:v1.0.0

docker tag ai-chatbot-frontend:latest yourusername/ai-chatbot-frontend:latest
docker tag ai-chatbot-frontend:latest yourusername/ai-chatbot-frontend:v1.0.0
```

#### Push Images
```bash
# Push latest
docker push yourusername/ai-chatbot-backend:latest
docker push yourusername/ai-chatbot-frontend:latest

# Push versioned
docker push yourusername/ai-chatbot-backend:v1.0.0
docker push yourusername/ai-chatbot-frontend:v1.0.0
```

#### Pull Images
```bash
docker pull yourusername/ai-chatbot-backend:latest
docker pull yourusername/ai-chatbot-frontend:latest
```

### AWS Elastic Container Registry (ECR)

#### Setup
```bash
# Install AWS CLI
# https://aws.amazon.com/cli/

# Configure credentials
aws configure

# Create repositories
aws ecr create-repository --repository-name ai-chatbot-backend --region us-east-1
aws ecr create-repository --repository-name ai-chatbot-frontend --region us-east-1
```

#### Login
```bash
# Get login password and authenticate
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com
```

#### Tag Images
```bash
# Format: account-id.dkr.ecr.region.amazonaws.com/repository:tag
docker tag ai-chatbot-backend:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/ai-chatbot-backend:latest
docker tag ai-chatbot-frontend:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/ai-chatbot-frontend:latest
```

#### Push Images
```bash
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/ai-chatbot-backend:latest
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/ai-chatbot-frontend:latest
```

#### Pull Images
```bash
docker pull 123456789012.dkr.ecr.us-east-1.amazonaws.com/ai-chatbot-backend:latest
docker pull 123456789012.dkr.ecr.us-east-1.amazonaws.com/ai-chatbot-frontend:latest
```

### Google Container Registry (GCR)

#### Setup
```bash
# Install Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# Authenticate
gcloud auth login

# Configure Docker
gcloud auth configure-docker

# Set project
gcloud config set project YOUR_PROJECT_ID
```

#### Tag Images
```bash
# Format: gcr.io/project-id/image:tag
docker tag ai-chatbot-backend:latest gcr.io/your-project-id/ai-chatbot-backend:latest
docker tag ai-chatbot-frontend:latest gcr.io/your-project-id/ai-chatbot-frontend:latest
```

#### Push Images
```bash
docker push gcr.io/your-project-id/ai-chatbot-backend:latest
docker push gcr.io/your-project-id/ai-chatbot-frontend:latest
```

#### Pull Images
```bash
docker pull gcr.io/your-project-id/ai-chatbot-backend:latest
docker pull gcr.io/your-project-id/ai-chatbot-frontend:latest
```

### Azure Container Registry (ACR)

#### Setup
```bash
# Install Azure CLI
# https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# Login
az login

# Create registry
az acr create --resource-group myResourceGroup --name myregistry --sku Basic

# Login to registry
az acr login --name myregistry
```

#### Tag Images
```bash
# Format: registry.azurecr.io/repository:tag
docker tag ai-chatbot-backend:latest myregistry.azurecr.io/ai-chatbot-backend:latest
docker tag ai-chatbot-frontend:latest myregistry.azurecr.io/ai-chatbot-frontend:latest
```

#### Push Images
```bash
docker push myregistry.azurecr.io/ai-chatbot-backend:latest
docker push myregistry.azurecr.io/ai-chatbot-frontend:latest
```

#### Pull Images
```bash
docker pull myregistry.azurecr.io/ai-chatbot-backend:latest
docker pull myregistry.azurecr.io/ai-chatbot-frontend:latest
```

### GitHub Container Registry (GHCR)

#### Setup
```bash
# Create personal access token with write:packages scope
# https://github.com/settings/tokens

# Login
echo YOUR_TOKEN | docker login ghcr.io -u YOUR_USERNAME --password-stdin
```

#### Tag Images
```bash
# Format: ghcr.io/username/repository:tag
docker tag ai-chatbot-backend:latest ghcr.io/yourusername/ai-chatbot-backend:latest
docker tag ai-chatbot-frontend:latest ghcr.io/yourusername/ai-chatbot-frontend:latest
```

#### Push Images
```bash
docker push ghcr.io/yourusername/ai-chatbot-backend:latest
docker push ghcr.io/yourusername/ai-chatbot-frontend:latest
```

#### Pull Images
```bash
docker pull ghcr.io/yourusername/ai-chatbot-backend:latest
docker pull ghcr.io/yourusername/ai-chatbot-frontend:latest
```

## 🔄 CI/CD Integration

### GitHub Actions

Create `.github/workflows/docker-build-push.yml`:

```yaml
name: Build and Push Docker Images

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]

jobs:
  build-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push backend
        uses: docker/build-push-action@v4
        with:
          context: ./backend
          push: true
          tags: |
            yourusername/ai-chatbot-backend:latest
            yourusername/ai-chatbot-backend:${{ github.sha }}

  build-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Login to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push frontend
        uses: docker/build-push-action@v4
        with:
          context: ./frontend
          push: true
          tags: |
            yourusername/ai-chatbot-frontend:latest
            yourusername/ai-chatbot-frontend:${{ github.sha }}
```

### GitLab CI

Create `.gitlab-ci.yml`:

```yaml
stages:
  - build
  - push

build-backend:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t ai-chatbot-backend:latest ./backend
    - docker tag ai-chatbot-backend:latest $CI_REGISTRY_IMAGE/backend:$CI_COMMIT_SHA
    - docker push $CI_REGISTRY_IMAGE/backend:$CI_COMMIT_SHA

build-frontend:
  stage: build
  image: docker:latest
  services:
    - docker:dind
  script:
    - docker build -t ai-chatbot-frontend:latest ./frontend
    - docker tag ai-chatbot-frontend:latest $CI_REGISTRY_IMAGE/frontend:$CI_COMMIT_SHA
    - docker push $CI_REGISTRY_IMAGE/frontend:$CI_COMMIT_SHA
```

## 🏷️ Tagging Strategy

### Semantic Versioning
```bash
# Major.Minor.Patch
docker tag image:latest image:1.0.0
docker tag image:latest image:1.0
docker tag image:latest image:1
```

### Git-based Tags
```bash
# Commit SHA
docker tag image:latest image:$(git rev-parse --short HEAD)

# Branch name
docker tag image:latest image:$(git branch --show-current)

# Tag name
docker tag image:latest image:$(git describe --tags)
```

### Environment Tags
```bash
docker tag image:latest image:dev
docker tag image:latest image:staging
docker tag image:latest image:production
```

## 🔍 Verification

### Check Local Images
```bash
# List all images
docker images

# Filter by name
docker images | findstr ai-chatbot

# Check image details
docker inspect ai-chatbot-backend:latest
```

### Check Remote Images
```bash
# Docker Hub
curl https://hub.docker.com/v2/repositories/yourusername/ai-chatbot-backend/tags

# ECR
aws ecr describe-images --repository-name ai-chatbot-backend

# GCR
gcloud container images list --repository=gcr.io/your-project-id
```

### Test Images
```bash
# Run backend
docker run -p 8000:8000 --env-file backend/.env ai-chatbot-backend:latest

# Run frontend
docker run -p 3000:3000 --env-file frontend/.env.local ai-chatbot-frontend:latest

# Test health
curl http://localhost:8000/health
```

## 🧹 Cleanup

### Remove Local Images
```bash
# Remove specific image
docker rmi ai-chatbot-backend:latest

# Remove all versions
docker rmi $(docker images -q ai-chatbot-backend)

# Remove dangling images
docker image prune

# Remove all unused images
docker image prune -a
```

### Remove Remote Images
```bash
# Docker Hub (via web interface or API)
# ECR
aws ecr batch-delete-image --repository-name ai-chatbot-backend --image-ids imageTag=v1.0.0

# GCR
gcloud container images delete gcr.io/your-project-id/ai-chatbot-backend:v1.0.0
```

## 📊 Image Size Optimization

### Check Image Size
```bash
docker images ai-chatbot-backend
docker images ai-chatbot-frontend
```

### Analyze Layers
```bash
docker history ai-chatbot-backend:latest
```

### Use dive for detailed analysis
```bash
# Install dive
# https://github.com/wagoodman/dive

# Analyze image
dive ai-chatbot-backend:latest
```

## 🔐 Security Scanning

### Docker Scan
```bash
docker scan ai-chatbot-backend:latest
docker scan ai-chatbot-frontend:latest
```

### Trivy
```bash
# Install Trivy
# https://github.com/aquasecurity/trivy

# Scan image
trivy image ai-chatbot-backend:latest
```

### Snyk
```bash
# Install Snyk CLI
npm install -g snyk

# Authenticate
snyk auth

# Scan image
snyk container test ai-chatbot-backend:latest
```

## 📝 Best Practices

1. **Always tag with version** - Don't rely only on `latest`
2. **Use multi-stage builds** - Reduce image size
3. **Scan for vulnerabilities** - Before pushing to production
4. **Use .dockerignore** - Exclude unnecessary files
5. **Pin base image versions** - For reproducibility
6. **Sign images** - For security and verification
7. **Use private registries** - For sensitive applications
8. **Implement CI/CD** - Automate build and push
9. **Monitor image sizes** - Keep them minimal
10. **Document tags** - Maintain a tagging strategy

## 🎯 Quick Reference

```bash
# Build
docker build -t image:tag ./path

# Tag
docker tag source:tag target:tag

# Push
docker push registry/image:tag

# Pull
docker pull registry/image:tag

# Login
docker login registry

# Logout
docker logout registry
```

## 📚 Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Hub](https://hub.docker.com/)
- [AWS ECR Documentation](https://docs.aws.amazon.com/ecr/)
- [GCR Documentation](https://cloud.google.com/container-registry/docs)
- [ACR Documentation](https://docs.microsoft.com/en-us/azure/container-registry/)
