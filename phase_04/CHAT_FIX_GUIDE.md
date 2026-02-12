# Chat Route Fix Guide

## Status
✅ Backend chat endpoint is working (tested successfully)
✅ Login is working
❌ Frontend chat page showing connection issue

## What's Fixed
All API routes now use `BACKEND_URL` for Docker container communication:
- `/api/login` ✅
- `/api/logout` ✅
- `/api/session` ✅
- `/api/verify-token` ✅
- `/api/tasks` ✅
- `/api/chat/[userId]` ✅

## Testing Steps

### 1. Check if containers are running
```bash
docker ps --filter "name=ai-chatbot"
```

Should show both containers running.

### 2. Test backend directly
```bash
curl http://localhost:8000/health
```

Should return: `{"status":"healthy","service":"AI Chatbot with MCP"}`

### 3. Test frontend
Open browser: http://localhost:3000

### 4. Login
- Email: asfaqasim145@gmail.com
- Password: test123

### 5. Go to Chat
Navigate to: http://localhost:3000/chat

## Common Issues & Solutions

### Issue 1: "Connection issue" on chat page
**Cause**: Frontend health check failing

**Solution**: Check browser console (F12) for errors

### Issue 2: Chat API call fails
**Cause**: Token not being passed correctly

**Check**:
1. Open browser DevTools (F12)
2. Go to Network tab
3. Try sending a chat message
4. Look for `/api/chat/[userId]` request
5. Check if Authorization header is present

### Issue 3: CORS error
**Cause**: Backend not allowing frontend origin

**Solution**: Already fixed in docker-compose.yml:
```yaml
ALLOWED_ORIGINS=http://localhost:3000,http://frontend:3000
```

## Debug Commands

### View backend logs in real-time
```bash
docker logs ai-chatbot-backend -f
```

### View frontend logs in real-time
```bash
docker logs ai-chatbot-frontend -f
```

### Restart containers
```bash
docker-compose restart
```

### Rebuild and restart
```bash
docker-compose down
docker-compose up -d --build
```

## What to Check in Browser

1. Open http://localhost:3000/chat
2. Press F12 to open DevTools
3. Go to Console tab
4. Look for errors (red text)
5. Go to Network tab
6. Try sending a message
7. Look for failed requests (red)

## Expected Behavior

When you send a message in chat:
1. Frontend calls `/api/chat/[userId]` (Next.js API route)
2. Next.js API route calls `http://backend:8000/api/[userId]/chat`
3. Backend processes message with OpenAI
4. Response flows back to frontend
5. Message appears in chat

## If Still Not Working

Please provide:
1. Browser console errors (F12 → Console)
2. Network tab errors (F12 → Network)
3. Backend logs: `docker logs ai-chatbot-backend --tail 50`
4. Frontend logs: `docker logs ai-chatbot-frontend --tail 50`

## Quick Test Script

Run this to test the full flow:
```bash
python test_chat_docker.py
```

Should show:
- ✅ Login successful
- ✅ Chat successful
