# 🚀 Docker Quick Fix - Urdu Mein

## Current Situation

✅ **Frontend Container**: Chal raha hai (http://localhost:3000)  
❌ **Backend Container**: Nahi chal raha (database error)

## Problem

Backend container **Neon PostgreSQL database** use kar raha hai jismein **schema mismatch** hai:
- `user.id` = UUID type
- `task.user_id` = VARCHAR type  
- Dono match nahi kar rahe!

## ✨ Quick Solution

### Option 1: Sirf Frontend Use Karo (Abhi)

Frontend already chal raha hai! Browser mein jao:
```
http://localhost:3000
```

**Note**: Backend APIs kaam nahi karenge, lekin UI dekh sakte ho.

### Option 2: Backend Bhi Chalao (Database Fix Ke Saath)

Neon database mein jao aur ye SQL run karo:

```sql
-- Step 1: Purana task table delete karo
DROP TABLE IF EXISTS task CASCADE;

-- Step 2: Naya task table banao (sahi types ke saath)
CREATE TABLE task (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR NOT NULL,
    description VARCHAR,
    status VARCHAR NOT NULL DEFAULT 'pending',
    user_id UUID NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES "user"(id) ON DELETE CASCADE
);
```

Phir containers restart karo:
```bash
docker-compose down
docker-compose up -d
```

### Option 3: Local SQLite Use Karo (Sabse Aasan!)

Backend code mein SQLite already configured hai. Bas environment variable comment out karo.

## 🎯 Recommended: Option 3 (SQLite)

Ye sabse aasan hai local development ke liye:

1. **Docker Compose file already updated hai**
2. **Containers start karo**:
   ```bash
   docker-compose up -d
   ```
3. **Check karo**:
   ```bash
   docker ps
   ```

## 📱 Access URLs

Jab dono containers chal jayenge:
- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000  
- **API Docs**: http://localhost:8000/docs

## 🔍 Debug Commands

### Containers check karo:
```bash
docker ps -a
```

### Backend logs dekho:
```bash
docker logs ai-chatbot-backend
```

### Frontend logs dekho:
```bash
docker logs ai-chatbot-frontend
```

### Containers restart karo:
```bash
docker-compose restart
```

## ✅ Summary

**Abhi kya hai:**
- Frontend ✅ Running
- Backend ❌ Database error

**Kya karna hai:**
- Database schema fix karo (Option 2)
- Ya SQLite use karo (Option 3 - Recommended)

Phir dono containers perfectly chalenge! 🚀
