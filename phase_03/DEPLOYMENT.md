# Deployment Guide

## 1. Commit Code
```bash
git add backend/routes/tasks.py backend/src/api/routes/chat_simple.py .gitignore vercel.json
git commit -m "Fix: SQLite and PostgreSQL support"
git push
```

## 2. Vercel Setup
- Dashboard → Settings → General
- Root Directory: `frontend`
- Environment Variables: Copy from your local `.env` files
- Redeploy

## 3. Backend Deploy
- Use Railway or Render
- Root: `backend`
- Add environment variables
- Copy backend URL

## 4. Update Frontend
- Set `NEXT_PUBLIC_API_URL` to backend URL
- Redeploy

Done! ✅
