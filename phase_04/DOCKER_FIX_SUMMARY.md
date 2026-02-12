# Docker Deployment Fix Summary

## Problem
Frontend was unable to connect to backend when running in Docker containers. The error "Unable to connect to authentication service" appeared during login.

## Root Cause
The frontend API routes were using `NEXT_PUBLIC_API_URL=http://localhost:8000` for server-side API calls. Inside Docker containers, `localhost` refers to the container itself, not the host machine or other containers.

## Solution
Updated all frontend API routes to use `BACKEND_URL` environment variable for server-side (container-to-container) communication:

### Files Updated
1. `frontend/app/api/login/route.ts`
2. `frontend/app/api/logout/route.ts`
3. `frontend/app/api/session/route.ts`
4. `frontend/app/api/verify-token/route.ts`
5. `frontend/app/api/tasks/route.ts`
6. `frontend/app/api/chat/[userId]/route.ts`

### Change Applied
```typescript
// OLD (doesn't work in Docker)
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// NEW (works in Docker and local development)
const API_URL = process.env.BACKEND_URL || process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
```

## Environment Variables

### docker-compose.yml Configuration
```yaml
frontend:
  environment:
    - NEXT_PUBLIC_API_URL=http://localhost:8000  # For browser-side calls
    - BACKEND_URL=http://backend:8000             # For server-side calls (NEW)
```

## How It Works

### Network Flow
1. **Browser → Frontend**: User accesses `http://localhost:3000`
2. **Browser → Backend (direct)**: Client-side code uses `NEXT_PUBLIC_API_URL=http://localhost:8000`
3. **Frontend → Backend (server-side)**: API routes use `BACKEND_URL=http://backend:8000`

### Docker Networking
- Both containers are on the same Docker network (`app-network`)
- Containers can communicate using service names as hostnames
- `backend` resolves to the backend container's IP address
- Port mapping allows host machine to access containers via `localhost`

## Deployment Scripts

### 1. DEPLOY_DOCKER_FIXED.bat
Complete deployment script that:
- Stops existing containers
- Rebuilds images with latest code
- Starts containers
- Checks health and logs

### 2. TEST_DOCKER_DEPLOYMENT.bat
Testing script that:
- Verifies containers are running
- Tests backend health endpoint
- Tests frontend homepage
- Checks logs for errors

### 3. SIMPLE_DOCKER_DEPLOY.bat
Quick deployment script for rapid iteration

## Usage

### Deploy Application
```bash
DEPLOY_DOCKER_FIXED.bat
```

### Test Deployment
```bash
TEST_DOCKER_DEPLOYMENT.bat
```

### View Logs
```bash
# Backend logs
docker logs ai-chatbot-backend -f

# Frontend logs
docker logs ai-chatbot-frontend -f
```

### Stop Application
```bash
docker-compose down
```

## Testing the Fix

1. Run `DEPLOY_DOCKER_FIXED.bat`
2. Wait for containers to start (15 seconds)
3. Open http://localhost:3000
4. Try to sign up or login
5. Create a task
6. Test the chat feature

## Expected Results
- ✅ Login should work without "Unable to connect" error
- ✅ Tasks should be created and fetched from backend
- ✅ Chat should work with AI responses
- ✅ All API calls should succeed

## Troubleshooting

### If login still fails:
```bash
# Check backend logs
docker logs ai-chatbot-backend --tail 50

# Check if backend is receiving requests
docker logs ai-chatbot-backend -f
# Then try to login and watch for incoming requests
```

### If containers won't start:
```bash
# Check container status
docker ps -a

# Check specific container logs
docker logs ai-chatbot-backend
docker logs ai-chatbot-frontend
```

### If port conflicts:
```bash
# Check what's using port 8000 or 3000
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# Stop conflicting processes or change ports in docker-compose.yml
```

## Why Kubernetes Was Skipped

Kubernetes adds complexity for local development:
- Requires Minikube or similar cluster
- Complex networking (NodePort, port-forwarding)
- Harder to debug
- Slower iteration cycle

Docker Compose is better for local development:
- Simple networking
- Easy to debug
- Fast rebuild and restart
- Direct port mapping

## Production Deployment

For production, consider:
- Using Kubernetes or cloud services (AWS ECS, Google Cloud Run)
- Setting up proper ingress/load balancer
- Using managed databases (not SQLite)
- Implementing proper secrets management
- Setting up CI/CD pipelines

## Next Steps

1. ✅ Docker deployment working
2. Test all features thoroughly
3. Set up production environment variables
4. Deploy to cloud platform (Vercel, Railway, AWS, etc.)
5. Set up monitoring and logging
