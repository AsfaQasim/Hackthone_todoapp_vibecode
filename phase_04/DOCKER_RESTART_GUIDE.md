# Docker Desktop Restart Karo

## Step 1: Docker Desktop Band Karo
- Task Manager kholo (Ctrl + Shift + Esc)
- "Docker Desktop" process ko End Task karo
- Ya simply Docker Desktop close karo

## Step 2: Docker Desktop Phir Se Start Karo
- Start Menu se "Docker Desktop" search karo
- Open karo
- Wait karo jab tak "Docker Desktop is running" show na ho

## Step 3: Containers Start Karo

### Option A: Docker Desktop UI Se
1. Containers tab kholo
2. `ai-chatbot-backend` container pe click karo → Start button dabao
3. `ai-chatbot-frontend` container pe click karo → Start button dabao

### Option B: Terminal Se (Naya Terminal Kholo)
```cmd
docker ps -a
docker start ai-chatbot-backend
docker start ai-chatbot-frontend
docker ps
```

## Step 4: Test Karo
- Backend: http://localhost:8000/health
- Frontend: http://localhost:3000

---

## Agar Containers Nahi Dikhe:

```cmd
docker-compose up -d
```

## Logs Check Karo:
```cmd
docker logs ai-chatbot-backend
docker logs ai-chatbot-frontend
```
