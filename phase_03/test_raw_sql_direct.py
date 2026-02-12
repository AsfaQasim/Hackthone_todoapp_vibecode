"""Direct test of raw SQL query"""
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

# Database connection
DATABASE_URL = "sqlite:///backend/todo_app_local.db"
engine = create_engine(DATABASE_URL)

USER_ID = "65d85bae-6ae6-4f9d-be8c-d149a177f8fc"

print("Testing raw SQL query directly...")
print("=" * 70)

with Session(engine) as session:
    # Test the exact query from the code
    query_text = text("SELECT * FROM tasks WHERE user_id = :user_id")
    result = session.execute(query_text, {"user_id": USER_ID})
    
    rows = result.fetchall()
    print(f"✅ Found {len(rows)} tasks")
    
    if rows:
        print("\nTasks:")
        for i, row in enumerate(rows[:5], 1):
            print(f"{i}. ID: {row[0]}")
            print(f"   Title: {row[1]}")
            print(f"   Status: {row[3]}")
            print(f"   User ID: {row[4]}")
            print()
    else:
        print("❌ No tasks found!")
        
        # Try without parameter
        print("\nTrying direct query...")
        query2 = text(f"SELECT * FROM tasks WHERE user_id = '{USER_ID}'")
        result2 = session.execute(query2)
        rows2 = result2.fetchall()
        print(f"Direct query found: {len(rows2)} tasks")

print("=" * 70)
print("\n⚠️  If this shows tasks but API doesn't, backend needs restart!")
print("Run: cd backend && uvicorn main:app --reload")
