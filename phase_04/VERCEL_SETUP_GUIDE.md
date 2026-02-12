# Vercel Deployment Setup Guide

## ✅ What's Done:
1. Backend deployed at: `https://hackthone-todoapp-vibecode-nudz.vercel.app`
2. All frontend API routes updated to use `process.env.NEXT_PUBLIC_API_URL`
3. Code committed locally

## 🔧 Next Steps for Vercel Frontend Deployment:

### Step 1: Add Environment Variable in Vercel
1. Go to your Vercel dashboard
2. Select your frontend project
3. Go to **Settings** → **Environment Variables**
4. Add this variable:
   - **Name**: `NEXT_PUBLIC_API_URL`
   - **Value**: `https://hackthone-todoapp-vibecode-nudz.vercel.app`
   - **Environment**: Select all (Production, Preview, Development)
5. Click **Save**

### Step 2: Push Code to GitHub
Run these commands:
```bash
cd F:\hackthone_todo_vibecode
git push origin main
```

If push fails due to repository rules, try:
```bash
git push origin main --no-verify
```

### Step 3: Redeploy Frontend
After pushing, Vercel will automatically redeploy. Or manually:
1. Go to Vercel dashboard
2. Select your frontend project
3. Click **Deployments** tab
4. Click **Redeploy** on the latest deployment

## 🧪 Testing After Deployment:

### Test Backend:
```bash
python test_backend_health.py
```

### Test Frontend:
1. Open your deployed frontend URL
2. Try to login with: `asfaqasim145@gmail.com`
3. Go to AI Assistant page
4. Try creating a task via chat

## 📝 Local Development:
For local development, change `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Then restart your frontend:
```bash
cd frontend
npm run dev
```

## 🔍 Files Changed:
- `frontend/app/api/login/route.ts` ✅
- `frontend/app/api/logout/route.ts` ✅
- `frontend/app/api/session/route.ts` ✅
- `frontend/app/api/tasks/route.ts` ✅
- `frontend/app/api/chat/[userId]/route.ts` ✅
- `frontend/app/api/verify-token/route.ts` ✅
- `frontend/.env.local` ✅

All files now use: `const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';`
