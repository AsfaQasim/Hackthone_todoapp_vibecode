# Docker Containers Ko Manually Start Karo

## Step 1: Docker Desktop Kholo

## Step 2: Containers Tab Mein Jao

## Step 3: In Containers Ko Start Karo:
1. **ai-chatbot-backend** - Start button dabao
2. **ai-chatbot-frontend** - Start button dabao

## Step 4: Check Karo
- Backend: http://localhost:8000/health
- Frontend: http://localhost:3000

---

## Ya Terminal Se:

```cmd
docker start ai-chatbot-backend
docker start ai-chatbot-frontend
```

## Containers Check Karo:
```cmd
docker ps
```

## Logs Check Karo:
```cmd
docker logs ai-chatbot-backend
docker logs ai-chatbot-frontend
```
