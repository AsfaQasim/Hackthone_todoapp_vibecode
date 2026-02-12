# Docker Architecture Diagram

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         Docker Host                              │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    Docker Compose                           │ │
│  │                  (Orchestration Layer)                      │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
│  ┌──────────────────────────┐  ┌──────────────────────────┐    │
│  │   Frontend Container     │  │   Backend Container      │    │
│  │   ┌──────────────────┐   │  │   ┌──────────────────┐   │    │
│  │   │   Next.js App    │   │  │   │  FastAPI App     │   │    │
│  │   │   Port: 3000     │   │  │   │  Port: 8000      │   │    │
│  │   │   Node 20 Alpine │   │  │   │  Python 3.11     │   │    │
│  │   └──────────────────┘   │  │   └──────────────────┘   │    │
│  │                          │  │                          │    │
│  │   Environment:           │  │   Environment:           │    │
│  │   - NEXT_PUBLIC_API_URL  │  │   - DATABASE_URL         │    │
│  │   - DATABASE_URL         │  │   - JWT_SECRET           │    │
│  │   - JWT_SECRET           │  │   - OPENAI_API_KEY       │    │
│  │                          │  │   - ALLOWED_ORIGINS      │    │
│  └──────────────────────────┘  └──────────────────────────┘    │
│           │                              │                       │
│           │                              │                       │
│           └──────────────┬───────────────┘                       │
│                          │                                       │
│                  ┌───────▼────────┐                             │
│                  │  app-network   │                             │
│                  │  (Bridge)      │                             │
│                  └────────────────┘                             │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │                    Volumes                                  │ │
│  │   - backend-data (persistent storage)                      │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
                          │
                          │
                          ▼
        ┌─────────────────────────────────┐
        │   External Services             │
        │   - PostgreSQL (Neon)           │
        │   - OpenAI API                  │
        └─────────────────────────────────┘
```

## Container Details

### Frontend Container (Next.js)

```
┌─────────────────────────────────────────┐
│  ai-chatbot-frontend                    │
├─────────────────────────────────────────┤
│  Base Image: node:20-alpine             │
│  Size: ~150MB                           │
│  Port: 3000                             │
│  User: nextjs (non-root)                │
│                                         │
│  Layers:                                │
│  1. Dependencies (npm ci)               │
│  2. Build (npm run build)               │
│  3. Runtime (standalone)                │
│                                         │
│  Health Check:                          │
│  - Endpoint: /api/health                │
│  - Interval: 30s                        │
│  - Timeout: 10s                         │
│                                         │
│  Restart Policy: unless-stopped         │
└─────────────────────────────────────────┘
```

### Backend Container (FastAPI)

```
┌─────────────────────────────────────────┐
│  ai-chatbot-backend                     │
├─────────────────────────────────────────┤
│  Base Image: python:3.11-slim           │
│  Size: ~200MB                           │
│  Port: 8000                             │
│  User: root (can be changed)            │
│                                         │
│  Layers:                                │
│  1. System dependencies                 │
│  2. Python packages                     │
│  3. Application code                    │
│                                         │
│  Health Check:                          │
│  - Endpoint: /health                    │
│  - Interval: 30s                        │
│  - Timeout: 10s                         │
│                                         │
│  Restart Policy: unless-stopped         │
└─────────────────────────────────────────┘
```

## Network Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    External Access                        │
│                                                           │
│  Browser ──────────────────────────────────────────────┐ │
│                                                         │ │
└─────────────────────────────────────────────────────────┼─┘
                                                          │
                                                          │
┌─────────────────────────────────────────────────────────▼─┐
│                    Docker Host Network                    │
│                                                            │
│  Port 3000 ────────────────────────┐                      │
│  Port 8000 ──────────────────┐     │                      │
│                              │     │                      │
└──────────────────────────────┼─────┼──────────────────────┘
                               │     │
                               │     │
┌──────────────────────────────┼─────┼──────────────────────┐
│              app-network (Bridge Network)                 │
│                              │     │                      │
│  ┌───────────────────────────▼─┐ ┌▼──────────────────┐   │
│  │  backend:8000               │ │  frontend:3000    │   │
│  │  (Internal DNS)             │ │  (Internal DNS)   │   │
│  └─────────────────────────────┘ └───────────────────┘   │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

## Data Flow

### User Request Flow

```
1. User Browser
   │
   ├─→ http://localhost:3000
   │   │
   │   ▼
   │   Frontend Container (Next.js)
   │   │
   │   ├─→ Static Pages (SSG)
   │   │
   │   └─→ API Routes
   │       │
   │       ▼
   │       http://localhost:8000/api/*
   │       │
   │       ▼
   │       Backend Container (FastAPI)
   │       │
   │       ├─→ Authentication
   │       ├─→ Task Management
   │       ├─→ Chat (OpenAI)
   │       │
   │       ▼
   │       External Services
   │       ├─→ PostgreSQL (Neon)
   │       └─→ OpenAI API
   │
   └─→ Response back to browser
```

### Internal Communication

```
Frontend Container ←──────────────→ Backend Container
     (Next.js)      HTTP Requests      (FastAPI)
                    JSON Responses
                                           │
                                           │
                                           ▼
                                    External Services
                                    ├─→ Database
                                    └─→ OpenAI
```

## Build Process

### Multi-Stage Build (Frontend)

```
Stage 1: Dependencies
┌─────────────────────────┐
│ node:20-alpine          │
│ - Copy package files    │
│ - npm ci                │
│ Size: ~500MB            │
└─────────────────────────┘
           │
           ▼
Stage 2: Builder
┌─────────────────────────┐
│ node:20-alpine          │
│ - Copy dependencies     │
│ - Copy source code      │
│ - npm run build         │
│ Size: ~800MB            │
└─────────────────────────┘
           │
           ▼
Stage 3: Runner (Final)
┌─────────────────────────┐
│ node:20-alpine          │
│ - Copy built files only │
│ - Standalone output     │
│ Size: ~150MB ✓          │
└─────────────────────────┘
```

### Single-Stage Build (Backend)

```
┌─────────────────────────┐
│ python:3.11-slim        │
│ - System dependencies   │
│ - Python packages       │
│ - Application code      │
│ Size: ~200MB            │
└─────────────────────────┘
```

## Deployment Scenarios

### Local Development

```
Developer Machine
├─→ docker-compose up -d
│   ├─→ Build images (if needed)
│   ├─→ Create network
│   ├─→ Start containers
│   └─→ Mount volumes
│
└─→ Access: localhost:3000
```

### Production (Cloud)

```
Container Registry
├─→ Docker Hub
├─→ AWS ECR
├─→ Google GCR
└─→ Azure ACR
    │
    ▼
Cloud Platform
├─→ AWS ECS/Fargate
├─→ Google Cloud Run
├─→ Azure Container Instances
└─→ Kubernetes (any cloud)
    │
    ▼
Load Balancer
    │
    ▼
Multiple Container Instances
├─→ Frontend (scaled)
└─→ Backend (scaled)
```

## Resource Allocation

### Default Resources

```
Frontend Container:
├─→ CPU: Unlimited (can be limited)
├─→ Memory: Unlimited (can be limited)
└─→ Disk: ~150MB (image) + runtime

Backend Container:
├─→ CPU: Unlimited (can be limited)
├─→ Memory: Unlimited (can be limited)
└─→ Disk: ~200MB (image) + runtime
```

### Recommended Limits (Production)

```yaml
Frontend:
  CPU: 0.5-1 core
  Memory: 512MB-1GB

Backend:
  CPU: 1-2 cores
  Memory: 1GB-2GB
```

## Security Layers

```
┌─────────────────────────────────────────┐
│  1. Network Isolation                   │
│     - Internal bridge network           │
│     - No direct external access         │
└─────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  2. Container Isolation                 │
│     - Separate namespaces               │
│     - Resource limits                   │
└─────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  3. User Permissions                    │
│     - Non-root user (frontend)          │
│     - Limited capabilities              │
└─────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────┐
│  4. Environment Variables               │
│     - Secrets not in images             │
│     - Runtime injection                 │
└─────────────────────────────────────────┘
```

## Monitoring Points

```
Container Level:
├─→ CPU usage
├─→ Memory usage
├─→ Network I/O
└─→ Disk I/O

Application Level:
├─→ Health checks
├─→ Application logs
├─→ Error rates
└─→ Response times

Infrastructure Level:
├─→ Container restarts
├─→ Image pull times
└─→ Volume usage
```

## Scaling Strategy

### Horizontal Scaling

```
Load Balancer
      │
      ├─→ Frontend Instance 1
      ├─→ Frontend Instance 2
      └─→ Frontend Instance 3
            │
            ├─→ Backend Instance 1
            ├─→ Backend Instance 2
            └─→ Backend Instance 3
                  │
                  └─→ Shared Database
```

### Vertical Scaling

```
Increase Resources:
├─→ More CPU cores
├─→ More memory
└─→ Faster storage
```

## Backup Strategy

```
Volumes:
├─→ backend-data
│   └─→ Backup: tar/rsync
│
Configuration:
├─→ .env.docker
│   └─→ Backup: version control (encrypted)
│
Images:
└─→ Container Registry
    └─→ Multiple versions/tags
```

This architecture provides a scalable, secure, and maintainable deployment solution for the AI Chatbot application.
