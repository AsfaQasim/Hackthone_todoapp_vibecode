# 🚀 START KARO ABHI - SIMPLE GUIDE (URDU)

## Problem Mil Gaya!
**BACKEND CHAL HI NAHI RAHA HAI!**

Isliye "Failed to fetch" error aa raha hai.

---

## ✅ SOLUTION - Backend Aur Frontend Start Karo

### Step 1: Backend Start Karo

**Command Prompt kholo aur ye run karo:**
```bash
cd F:\hackthone_todo_vibecode\phase_03\backend
python -m uvicorn main:app --reload
```

**Ye message ka wait karo:**
```
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Is terminal ko KHULA rakho!** Band mat karo.

---

### Step 2: Frontend Start Karo

**DOOSRA Command Prompt kholo aur ye run karo:**
```bash
cd F:\hackthone_todo_vibecode\phase_03\frontend
npm run dev
```

**Ye message ka wait karo:**
```
✓ Ready in 2.5s
○ Local: http://localhost:3000
```

**Is terminal ko bhi KHULA rakho!**

---

### Step 3: Browser Me Test Karo

1. Browser kholo: http://localhost:3000/login
2. Login karo: asfaqasim145@gmail.com / test123
3. Jao: http://localhost:3000/general-task-execution
4. Tasks dikhne chahiye!

---

## 🎯 Quick Commands (Copy-Paste Karo)

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

## ⚠️ Important Points

1. **Dono terminals khule rakho** jab tak app use kar rahe ho
2. **Band mat karo** warna app kaam karna band kar dega
3. **Agar errors aayein**, unhe padho aur mujhe batao

---

## 🔍 Kaise Pata Chalega Kaam Kar Raha Hai?

**Backend terminal me ye dikhna chahiye:**
```
INFO:     Application startup complete.
```

**Frontend terminal me ye dikhna chahiye:**
```
✓ Ready in 2.5s
```

**Browser me ye hona chahiye:**
- Login page kaam kare
- Tasks page tasks dikhaaye (not "Failed to fetch")

---

## 📋 Agar Problem Aaye

### Agar backend start nahi ho:
```bash
# Purane Python processes kill karo
taskkill /F /IM python.exe

# Phir se try karo
cd backend
python -m uvicorn main:app --reload
```

### Agar frontend start nahi ho:
```bash
# Purane Node processes kill karo
taskkill /F /IM node.exe

# Phir se try karo
cd frontend
npm run dev
```

### Agar port 8000 busy hai:
```bash
# Dekho kaun use kar raha hai
netstat -ano | findstr :8000

# Us process ko kill karo (PID number se replace karo)
taskkill /F /PID <PID>
```

---

## ✅ Success Checklist

- [ ] Backend terminal khula hai aur "Application startup complete" dikha raha hai
- [ ] Frontend terminal khula hai aur "Ready" dikha raha hai
- [ ] Browser me http://localhost:3000 khul raha hai
- [ ] Login kaam kar raha hai
- [ ] Tasks page tasks dikha raha hai (not "Failed to fetch")

---

## 🎯 Summary

**Problem:** Backend running hi nahi tha
**Solution:** Backend aur Frontend dono start karo
**How:** Do alag terminals me commands run karo

---

**BACKEND AUR FRONTEND AB START KARO!**

Upar diye gaye commands use karo do alag terminals me.

---

## 💡 Pro Tip

Agar bar bar start karna padta hai, to ye batch files use kar sakte ho:

**Backend ke liye:** `start_backend_fixed.bat`
**Frontend ke liye:** Naya batch file bana sakte hain

Ya phir dono terminals ko hamesha khula rakho jab kaam kar rahe ho!
