# Final Deployment Guide

## Backend - Render.com (FREE)

1. Go to https://render.com
2. Sign up with GitHub
3. New → Web Service
4. Connect your repo: `Hackthone_todoapp_vibecode`
5. Configure:
   - Name: `todo-backend`
   - Root Directory: `phase_03/backend`
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Environment Variables (copy from your `.env`):
   - `DATABASE_URL`
   - `BETTER_AUTH_SECRET`
   - `JWT_SECRET`
   - `OPENAI_API_KEY`
   - `ALLOWED_ORIGINS=*`
   - `ENVIRONMENT=production`
7. Click **Create Web Service**
8. Wait 5-10 minutes
9. Copy your Render URL (e.g., `https://todo-backend.onrender.com`)

## Frontend - Vercel

1. Delete current Vercel project
2. New Project → Import from GitHub
3. Select repo
4. Configure:
   - Root Directory: `phase_03/frontend` (manually type)
   - Framework: Next.js
   - Build Command: `npm run build`
   - Output Directory: `.next`
5. Environment Variables:
   - `NEXT_PUBLIC_API_URL=https://todo-backend.onrender.com` (your Render URL)
   - `DATABASE_URL` (same as backend)
   - `BETTER_AUTH_SECRET` (same as backend)
   - `JWT_SECRET` (same as backend)
   - `OPENAI_API_KEY` (same as backend)
   - `ENVIRONMENT=production`
6. Deploy

## Done!

- Backend: https://todo-backend.onrender.com
- Frontend: https://your-app.vercel.app

Both will work perfectly! 🚀

## Local Testing (Always works)
```bash
# Backend
cd backend
uvicorn main:app --reload

# Frontend
cd frontend
npm run dev
```

Local: http://localhost:3000 ✅
