# 🚀 Quick Setup Guide - Urdu/English

## ✅ Kya Ho Gaya Hai (What's Done):

1. **Backend Deploy** ✅
   - URL: `https://hackthone-todoapp-vibecode-nudz.vercel.app`
   - Health check working
   - All APIs working

2. **Frontend Code Fix** ✅
   - All API routes ab environment variable use kar rahe hain
   - Code GitHub pe push ho gaya hai
   - Local aur production dono ke liye ready

## 🔧 Ab Kya Karna Hai (What to Do Now):

### Step 1: Vercel Environment Variable Add Karo

1. Vercel dashboard kholo: https://vercel.com/dashboard
2. Apna **frontend project** select karo
3. **Settings** → **Environment Variables** pe jao
4. Ye variable add karo:
   ```
   Name: NEXT_PUBLIC_API_URL
   Value: https://hackthone-todoapp-vibecode-nudz.vercel.app
   ```
5. **All environments** select karo (Production, Preview, Development)
6. **Save** karo

### Step 2: Frontend Redeploy Karo

Vercel automatically redeploy kar dega, ya manually:
1. **Deployments** tab pe jao
2. Latest deployment pe **Redeploy** click karo

### Step 3: Test Karo

Frontend deploy hone ke baad:
1. Deployed URL kholo
2. Login karo: `asfaqasim145@gmail.com`
3. AI Assistant page pe jao
4. Task create karo via chat

## 🏠 Local Development Ke Liye:

Agar local pe test karna hai:

1. `frontend/.env.local` file me ye change karo:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

2. Backend start karo:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

3. Frontend start karo:
   ```bash
   cd frontend
   npm run dev
   ```

## 📊 Test Script:

Backend test karne ke liye:
```bash
python test_backend_health.py
```

Full deployment test:
```bash
python test_full_deployment.py
```

## 🎯 Summary:

**Local pe chalne ke liye:**
- `.env.local` me `NEXT_PUBLIC_API_URL=http://localhost:8000`
- Backend aur frontend dono locally run karo

**Production pe chalne ke liye:**
- Vercel me `NEXT_PUBLIC_API_URL=https://hackthone-todoapp-vibecode-nudz.vercel.app`
- Frontend redeploy karo

**Dono jagah same code chalega!** ✨
