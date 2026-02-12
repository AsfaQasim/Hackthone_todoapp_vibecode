"""Check which users exist in database and their tasks"""
import os
from sqlalchemy import create_engine, text

# Get database URL from environment
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://neondb_owner:npg_6DzBwoCp1Muf@ep-holy-flower-ahrkffp6-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require')

print("=" * 80)
print("🔍 CHECKING DATABASE USERS AND TASKS")
print("=" * 80)

try:
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # Get all users
        print("\n1️⃣ Users in database:")
        result = conn.execute(text("SELECT id, email, name FROM users ORDER BY created_at DESC LIMIT 10"))
        users = result.fetchall()
        
        if users:
            for i, user in enumerate(users, 1):
                print(f"   {i}. Email: {user[1]}")
                print(f"      ID: {user[0]}")
                print(f"      Name: {user[2]}")
                print()
        else:
            print("   ⚠️  No users found!")
        
        # Get all tasks
        print("\n2️⃣ Tasks in database:")
        result = conn.execute(text("SELECT id, title, status, user_id FROM tasks ORDER BY created_at DESC LIMIT 10"))
        tasks = result.fetchall()
        
        if tasks:
            for i, task in enumerate(tasks, 1):
                print(f"   {i}. Title: {task[1]}")
                print(f"      ID: {task[0]}")
                print(f"      Status: {task[2]}")
                print(f"      User ID: {task[3]}")
                print()
        else:
            print("   ⚠️  No tasks found!")
        
        # Count tasks per user
        print("\n3️⃣ Tasks per user:")
        result = conn.execute(text("""
            SELECT u.email, u.id, COUNT(t.id) as task_count
            FROM users u
            LEFT JOIN tasks t ON u.id = t.user_id
            GROUP BY u.id, u.email
            ORDER BY task_count DESC
        """))
        user_tasks = result.fetchall()
        
        if user_tasks:
            for i, row in enumerate(user_tasks, 1):
                print(f"   {i}. {row[0]}: {row[2]} tasks")
                print(f"      User ID: {row[1]}")
                print()
        
        # Find the user with email asfaqasim145@gmail.com
        print("\n4️⃣ Looking for asfaqasim145@gmail.com:")
        result = conn.execute(text("SELECT id, email, name FROM users WHERE email = :email"), {"email": "asfaqasim145@gmail.com"})
        user = result.fetchone()
        
        if user:
            print(f"   ✅ User found!")
            print(f"   ID: {user[0]}")
            print(f"   Email: {user[1]}")
            print(f"   Name: {user[2]}")
            
            # Get tasks for this user
            result = conn.execute(text("SELECT id, title, status FROM tasks WHERE user_id = :user_id"), {"user_id": str(user[0])})
            user_tasks = result.fetchall()
            
            print(f"\n   📋 Tasks for this user: {len(user_tasks)}")
            for i, task in enumerate(user_tasks[:5], 1):
                print(f"      {i}. {task[1]} ({task[2]})")
        else:
            print(f"   ⚠️  User not found in database!")
            print(f"   This is the problem - user needs to be created in database")
            
except Exception as e:
    print(f"❌ Database error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("📊 DIAGNOSIS")
print("=" * 80)
print("\nProblem: Login creates a NEW user ID every time instead of using existing user")
print("Solution: Need to fix login to check if user exists in database first")
print("=" * 80)
