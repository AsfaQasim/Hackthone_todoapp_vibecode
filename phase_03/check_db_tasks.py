"""Check database tasks directly"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables from backend/.env
load_dotenv('backend/.env')

# Get database URL from environment
db_url = os.getenv("DATABASE_URL")

print("=" * 80)
print("🔍 CHECKING DATABASE DIRECTLY")
print("=" * 80)
print(f"Database: {db_url[:50]}...")

engine = create_engine(db_url)

with engine.connect() as conn:
    # Check users
    print("\n1️⃣ Users in database:")
    result = conn.execute(text('SELECT id, email FROM "user"'))
    users = result.fetchall()
    for user in users:
        print(f"  - {user[1]} (ID: {user[0]})")
    
    # Check tasks
    print("\n2️⃣ Tasks in database:")
    result = conn.execute(text("SELECT id, title, user_id, status, created_at FROM task ORDER BY created_at DESC"))
    tasks = result.fetchall()
    
    if tasks:
        print(f"Found {len(tasks)} tasks:")
        for task in tasks:
            print(f"  - {task[1]}")
            print(f"    ID: {task[0]}")
            print(f"    User ID: {task[2]}")
            print(f"    Status: {task[3]}")
            print(f"    Created: {task[4]}")
            print()
    else:
        print("⚠️ No tasks found in database!")
    
    # Check tasks for specific user
    print("\n3️⃣ Tasks for asfaqasim145@gmail.com:")
    result = conn.execute(text('''
        SELECT t.id, t.title, t.user_id, t.status 
        FROM task t
        JOIN "user" u ON t.user_id = u.id
        WHERE u.email = :email
        ORDER BY t.created_at DESC
    '''), {"email": "asfaqasim145@gmail.com"})
    
    user_tasks = result.fetchall()
    if user_tasks:
        print(f"Found {len(user_tasks)} tasks:")
        for task in user_tasks:
            print(f"  - {task[1]} (Status: {task[3]})")
    else:
        print("⚠️ No tasks found for this user!")

print("\n" + "=" * 80)
