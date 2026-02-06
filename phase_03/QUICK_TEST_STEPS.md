# Quick Test Steps / فوری ٹیسٹ کے قدم

## Backend Logs Dekho / Check Backend Logs

Backend terminal mein ye dikhna chahiye jab reload ho:
```
INFO: Application startup complete.
```

## Test Karne Ka Tareeqa

### Step 1: Browser Console Kholo
```
Press F12
Go to Console tab
```

### Step 2: Chat Page Par Jao
```
http://localhost:3000/chat
```

### Step 3: Message Bhejo
```
Type: Add task: Test debugging
Press Enter
```

### Step 4: Backend Logs Dekho

Backend terminal mein ye dikhna chahiye:
```
============================================================
📨 Chat request from user 2: Add task: Test debugging
👤 Authenticated user: asfaqasim145@gmail.com (ID: xxx)
🔑 Using authenticated user ID: xxx
🎯 Task creation detected!
📝 Task title: Test debugging
✅ Task created successfully!
   ID: xxx
   Title: Test debugging
   User: xxx
✅ Response ready: ✅ I've created a new task: 'Test debugging'...
============================================================
```

### Step 5: Frontend Console Dekho

Browser console mein ye dikhna chahiye:
```
Tasks loaded: [...]
```

## Agar 401 Error Aaye

### Check 1: Token Dekho
```javascript
// Browser console mein:
document.cookie
// Should show: auth_token=...
```

### Check 2: Backend Logs Dekho
```
// Look for:
❌ Token has expired
// Or:
❌ No authorization header
```

### Check 3: Logout/Login Karo
```
1. Sidebar → Logout
2. Login page → Login again
3. Try again
```

## Agar Task Create Nahi Ho Raha

### Check Backend Logs For:
```
❌ Error creating task: ...
```

### Common Errors:

**Error 1**: "badly formed hexadecimal UUID string"
- **Meaning**: User ID format issue
- **Solution**: Backend ab handle kar raha hai

**Error 2**: "Token expired"
- **Meaning**: Token purana ho gaya
- **Solution**: Logout aur login karo

**Error 3**: "Not authenticated"
- **Meaning**: Token nahi mila
- **Solution**: Check cookies, phir se login karo

## Success Indicators / کامیابی کی علامات

✅ Backend logs show: "✅ Task created successfully!"
✅ Frontend shows: "✅ I've created a new task: '...'"
✅ No 401 error
✅ Task appears in /general-task-execution

## Next Steps

1. Test karo
2. Backend logs share karo
3. Browser console errors share karo
4. Mujhe batao kya ho raha hai!

---

**Ab test karo aur results batao!** 🚀
