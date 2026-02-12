"""Check actual database schema"""
import os
from sqlalchemy import create_engine, text, inspect
from dotenv import load_dotenv

# Load environment variables from backend/.env
load_dotenv('backend/.env')

# Get database URL from environment
db_url = os.getenv("DATABASE_URL")

print("=" * 80)
print("🔍 CHECKING DATABASE SCHEMA")
print("=" * 80)

engine = create_engine(db_url)

with engine.connect() as conn:
    # Get table columns
    print("\n📋 TASK TABLE SCHEMA:")
    result = conn.execute(text("""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = 'task'
        ORDER BY ordinal_position
    """))
    
    columns = result.fetchall()
    for col in columns:
        print(f"  - {col[0]}: {col[1]} (nullable: {col[2]})")
    
    # Get all tasks
    print("\n📋 ALL TASKS:")
    result = conn.execute(text("SELECT * FROM task ORDER BY created_at DESC LIMIT 10"))
    tasks = result.fetchall()
    
    if tasks:
        print(f"Found {len(tasks)} tasks")
        for task in tasks:
            print(f"\nTask: {task}")
    else:
        print("⚠️ No tasks found!")

print("\n" + "=" * 80)
