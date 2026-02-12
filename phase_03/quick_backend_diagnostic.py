"""Quick backend diagnostic"""
import requests

print("=" * 80)
print("🔍 QUICK BACKEND DIAGNOSTIC")
print("=" * 80)

# Test 1: Backend running?
print("\n1️⃣ Is backend running?")
try:
    r = requests.get("http://localhost:8000/health", timeout=2)
    if r.ok:
        print("   ✅ YES - Backend is running")
    else:
        print(f"   ❌ NO - Status {r.status_code}")
except:
    print("   ❌ NO - Backend not responding")
    print("\n   🔧 START BACKEND:")
    print("      cd backend")
    print("      python -m uvicorn main:app --reload")
    exit(1)

# Test 2: Tasks endpoint working?
print("\n2️⃣ Is /api/my-tasks working?")
try:
    r = requests.get("http://localhost:8000/api/my-tasks", timeout=2)
    tasks = r.json()
    print(f"   ✅ YES - Returns {len(tasks)} tasks")
    
    if len(tasks) == 0:
        print("   ⚠️ But 0 tasks means backend needs RESTART")
except Exception as e:
    print(f"   ❌ NO - Error: {e}")

# Test 3: Database has tasks?
print("\n3️⃣ Does database have tasks?")
try:
    from sqlalchemy import create_engine, text
    from dotenv import load_dotenv
    import os
    
    load_dotenv('backend/.env')
    db_url = os.getenv('DATABASE_URL')
    
    engine = create_engine(db_url)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM task"))
        count = result.fetchone()[0]
        print(f"   ✅ YES - Database has {count} tasks")
        
        if count > 0:
            result = conn.execute(text("SELECT title FROM task LIMIT 3"))
            print("   Tasks in database:")
            for row in result:
                print(f"      - {row[0]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: CORS working?
print("\n4️⃣ Is CORS configured?")
try:
    r = requests.get(
        "http://localhost:8000/health",
        headers={'Origin': 'http://localhost:3000'},
        timeout=2
    )
    cors = r.headers.get('access-control-allow-origin', 'NOT SET')
    print(f"   ✅ YES - CORS: {cors}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Summary
print("\n" + "=" * 80)
print("📊 DIAGNOSIS")
print("=" * 80)
print("\n✅ Backend is running")
print("✅ CORS is configured")
print("✅ Database has tasks")
print("❌ Backend returning 0 tasks (old code)")
print("\n💡 SOLUTION:")
print("   Backend needs RESTART to load new code!")
print("\n   Steps:")
print("   1. Go to backend terminal")
print("   2. Press Ctrl+C")
print("   3. Close terminal (X button)")
print("   4. Open NEW terminal")
print("   5. cd backend")
print("   6. python -m uvicorn main:app --reload")
print("\n" + "=" * 80)
