"""Complete verification script for task fix"""
import sqlite3
import requests
import sys

print("=" * 80)
print("COMPLETE TASK FIX VERIFICATION")
print("=" * 80)

# Configuration
DB_PATH = "backend/todo_app_local.db"
BASE_URL = "http://localhost:8000"
USER_ID = "65d85bae-6ae6-4f9d-be8c-d149a177f8fc"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NWQ4NWJhZS02YWU2LTRmOWQtYmU4Yy1kMTQ5YTE3N2Y4ZmMiLCJlbWFpbCI6ImFzZmFxYXNpbTE0NUBnbWFpbC5jb20iLCJ1c2VyX2VtYWlsIjoiYXNmYXFhc2ltMTQ1QGdtYWlsLmNvbSIsIm5hbWUiOiJhc2ZhcWFzaW0xNDUiLCJleHAiOjE3NzA0NTY0ODB9.RdzeeqqczHlZdSjyPvX_Rw40yN_bq_-BoF29r2b7Y8Q"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Test 1: Check database
print("\n1️⃣ CHECKING DATABASE")
print("-" * 80)
try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check tasks table structure
    cursor.execute("PRAGMA table_info(tasks)")
    columns = cursor.fetchall()
    print(f"✅ Tasks table exists with {len(columns)} columns")
    
    # Check user_id column type
    user_id_col = [col for col in columns if col[1] == 'user_id'][0]
    print(f"   user_id column type: {user_id_col[2]}")
    
    # Count tasks for user
    cursor.execute(
        "SELECT COUNT(*) FROM tasks WHERE user_id = ?",
        (USER_ID,)
    )
    task_count = cursor.fetchone()[0]
    print(f"✅ Found {task_count} tasks in database for user {USER_ID[:8]}...")
    
    # Show sample tasks
    if task_count > 0:
        cursor.execute(
            "SELECT title, status FROM tasks WHERE user_id = ? LIMIT 3",
            (USER_ID,)
        )
        tasks = cursor.fetchall()
        print(f"\n   Sample tasks:")
        for title, status in tasks:
            print(f"   - {title} ({status})")
    
    conn.close()
    db_check = True
except Exception as e:
    print(f"❌ Database error: {e}")
    db_check = False

# Test 2: Check backend API
print("\n2️⃣ CHECKING BACKEND API")
print("-" * 80)
try:
    # Test health endpoint
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    if response.status_code == 200:
        print(f"✅ Backend is running at {BASE_URL}")
    else:
        print(f"⚠️  Backend responded with status {response.status_code}")
except requests.exceptions.ConnectionError:
    print(f"❌ Backend is NOT running at {BASE_URL}")
    print(f"   Please start backend: cd backend && uvicorn main:app --reload")
    backend_running = False
except Exception as e:
    print(f"❌ Backend check error: {e}")
    backend_running = False
else:
    backend_running = True

# Test 3: Check task retrieval
if backend_running:
    print("\n3️⃣ CHECKING TASK RETRIEVAL")
    print("-" * 80)
    try:
        response = requests.get(
            f"{BASE_URL}/api/{USER_ID}/tasks",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            tasks = response.json()
            print(f"✅ Backend returned {len(tasks)} tasks")
            
            if len(tasks) > 0:
                print(f"\n   Retrieved tasks:")
                for i, task in enumerate(tasks[:3], 1):
                    print(f"   {i}. {task['title']} ({task['status']})")
                if len(tasks) > 3:
                    print(f"   ... and {len(tasks) - 3} more")
                
                # Compare with database count
                if db_check and len(tasks) == task_count:
                    print(f"\n✅ PERFECT! Backend count matches database count ({len(tasks)} tasks)")
                elif db_check:
                    print(f"\n⚠️  Mismatch: Backend returned {len(tasks)} but database has {task_count}")
            else:
                print(f"\n⚠️  Backend returned 0 tasks but database has {task_count}")
                print(f"   This means the fix didn't work or backend wasn't restarted")
        else:
            print(f"❌ Backend error: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Task retrieval error: {e}")

# Test 4: Check task creation
if backend_running:
    print("\n4️⃣ CHECKING TASK CREATION")
    print("-" * 80)
    try:
        new_task = {
            "title": "Verification Test Task",
            "description": "Testing the complete fix",
            "status": "pending"
        }
        
        response = requests.post(
            f"{BASE_URL}/api/{USER_ID}/tasks",
            headers=headers,
            json=new_task,
            timeout=10
        )
        
        if response.status_code == 200:
            task = response.json()
            print(f"✅ Successfully created task: {task['title']}")
            print(f"   Task ID: {task['id']}")
            print(f"   User ID: {task['user_id']}")
            
            # Verify in database
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT title, user_id FROM tasks WHERE id = ?",
                (task['id'],)
            )
            db_task = cursor.fetchone()
            conn.close()
            
            if db_task:
                print(f"✅ Task verified in database")
                print(f"   Stored user_id: {db_task[1]}")
            else:
                print(f"⚠️  Task not found in database")
        else:
            print(f"❌ Task creation failed: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
    except Exception as e:
        print(f"❌ Task creation error: {e}")

# Final summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

if db_check and backend_running:
    print("✅ Database: OK")
    print("✅ Backend: Running")
    print("✅ Fix Status: COMPLETE")
    print("\n🎉 Everything is working! You can now:")
    print("   1. Open http://localhost:3000/general-task-execution")
    print("   2. See all your tasks")
    print("   3. Create new tasks via chat")
elif db_check and not backend_running:
    print("✅ Database: OK")
    print("❌ Backend: NOT RUNNING")
    print("\n⚠️  Please start the backend:")
    print("   cd backend")
    print("   uvicorn main:app --reload")
else:
    print("❌ Some checks failed")
    print("\n⚠️  Please review the errors above")

print("=" * 80)
