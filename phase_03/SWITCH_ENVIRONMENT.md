# 🔄 Environment Switch Karne Ka Tareeqa

## ✅ Ab Kya Setup Hai:

1. **Local Development** → `.env.local` → `http://localhost:8000`
2. **Production (Vercel)** → `.env.production` → `https://hackthone-todoapp-vibecode-nudz.vercel.app`

## 🏠 Local Development (Apne Computer Pe):

### Step 1: Frontend .env.local Check Karo
File: `frontend/.env.local`
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Step 2: Backend Start Karo
```bash
cd backend
python -m uvicorn main:app --reload
```

### Step 3: Frontend Start Karo
```bash
cd frontend
npm run dev
```

### Step 4: Browser Me Test Karo
- Open: `http://localhost:3000`
- Login karo
- AI Assistant test karo

## 🌐 Production (Vercel Pe):

### Step 1: Vercel Environment Variables
Vercel dashboard me ye add karo:
```
NEXT_PUBLIC_API_URL = https://hackthone-todoapp-vibecode-nudz.vercel.app
```

### Step 2: Code Push Karo
```bash
git add .
git commit -m "Update environment configuration"
git push origin main
```

### Step 3: Vercel Automatic Deploy Karega
- Vercel automatically detect karega
- `.env.production` use karega
- Deploy ho jayega

### Step 4: Test Karo
- Deployed URL kholo
- Login karo
- AI Assistant test karo

## 🔧 Troubleshooting:

### Local Pe Kaam Nahi Kar Raha?
1. Backend running hai? Check: `http://localhost:8000/health`
2. Frontend running hai? Check: `http://localhost:3000`
3. `.env.local` me `localhost:8000` hai?
4. Frontend restart kiya?

### Vercel Pe Kaam Nahi Kar Raha?
1. Vercel me environment variable add kiya?
2. Code push kiya?
3. Deployment complete hui?
4. Backend URL sahi hai?

## 📝 Quick Commands:

### Local Development:
```bash
# Terminal 1 - Backend
cd backend
python -m uvicorn main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev

# Terminal 3 - Test
python check_backend_logs.py
```

### Production Deployment:
```bash
# Push code
git add .
git commit -m "Your message"
git push origin main

# Vercel automatically deploys!
```

## 🎯 Summary:

- **Local**: `.env.local` use hota hai → `localhost:8000`
- **Production**: `.env.production` use hota hai → Vercel URL
- **Dono alag hain**, isliye dono jagah kaam karega! ✨

---

**Important:** Frontend restart karna zaroori hai environment change ke baad!
