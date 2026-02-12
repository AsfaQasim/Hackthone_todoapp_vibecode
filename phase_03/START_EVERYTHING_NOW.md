# 🚀 START EVERYTHING NOW - SIMPLE GUIDE

## Problem Found!
**BACKEND IS NOT RUNNING!**

That's why you're getting "Failed to fetch" error.

---

## ✅ SOLUTION - Start Backend & Frontend

### Step 1: Start Backend

**Open Command Prompt and run:**
```bash
cd F:\hackthone_todo_vibecode\phase_03\backend
python -m uvicorn main:app --reload
```

**Wait for this message:**
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Keep this terminal open!** Don't close it.

---

### Step 2: Start Frontend

**Open ANOTHER Command Prompt and run:**
```bash
cd F:\hackthone_todo_vibecode\phase_03\frontend
npm run dev
```

**Wait for this message:**
```
✓ Ready in 2.5s
○ Local: http://localhost:3000
```

**Keep this terminal open too!**

---

### Step 3: Test in Browser

1. Open browser: http://localhost:3000/login
2. Login: asfaqasim145@gmail.com / test123
3. Go to: http://localhost:3000/general-task-execution
4. Should see tasks!

---

## 🎯 Quick Commands (Copy-Paste)

**Terminal 1 (Backend):**
```bash
cd F:\hackthone_todo_vibecode\phase_03\backend
python -m uvicorn main:app --reload
```

**Terminal 2 (Frontend):**
```bash
cd F:\hackthone_todo_vibecode\phase_03\frontend
npm run dev
```

---

## ⚠️ Important Notes

1. **Keep both terminals open** while using the app
2. **Don't close them** or app will stop working
3. **If you see errors**, read them and let me know

---

## 🔍 How to Know It's Working

**Backend terminal should show:**
```
INFO:     Application startup complete.
```

**Frontend terminal should show:**
```
✓ Ready in 2.5s
```

**Browser should show:**
- Login page works
- Tasks page shows tasks (not "Failed to fetch")

---

## 📋 Troubleshooting

### If backend won't start:
```bash
# Kill any existing Python processes
taskkill /F /IM python.exe

# Try starting again
cd backend
python -m uvicorn main:app --reload
```

### If frontend won't start:
```bash
# Kill any existing Node processes
taskkill /F /IM node.exe

# Try starting again
cd frontend
npm run dev
```

### If port 8000 is busy:
```bash
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill that process (replace PID with actual number)
taskkill /F /PID <PID>
```

---

## ✅ Success Checklist

- [ ] Backend terminal open and showing "Application startup complete"
- [ ] Frontend terminal open and showing "Ready"
- [ ] Browser can open http://localhost:3000
- [ ] Login works
- [ ] Tasks page shows tasks (not "Failed to fetch")

---

**START BACKEND AND FRONTEND NOW!**

Use the commands above in two separate terminals.
