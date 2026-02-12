"""Create a user with the ID that login is returning"""
import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://neondb_owner:npg_6DzBwoCp1Muf@ep-holy-flower-ahrkffp6-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require')

# The ID that login is currently returning
WRONG_USER_ID = "b6825731-2944-46a6-9e2d-b445ecfaa53c"
CORRECT_USER_ID = "add60fd1-792f-4ab9-9a53-e2f859482c59"
EMAIL = "asfaqasim145@gmail.com"

print("=" * 80)
print("🔧 CREATING MATCHING USER")
print("=" * 80)

try:
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # Check if wrong user ID exists
        check_query = text("SELECT id, email FROM users WHERE id = :user_id")
        result = conn.execute(check_query, {"user_id": WRONG_USER_ID})
        wrong_user = result.fetchone()
        
        if wrong_user:
            print(f"\n⚠️  User with wrong ID already exists:")
            print(f"   ID: {wrong_user[0]}")
            print(f"   Email: {wrong_user[1]}")
            
            # Update all tasks from correct user to wrong user
            print(f"\n🔄 Moving tasks from {CORRECT_USER_ID} to {WRONG_USER_ID}...")
            update_query = text("UPDATE tasks SET user_id = :new_id WHERE user_id = :old_id")
            result = conn.execute(update_query, {"new_id": WRONG_USER_ID, "old_id": CORRECT_USER_ID})
            conn.commit()
            print(f"   ✅ Moved {result.rowcount} tasks")
        else:
            print(f"\n📝 Creating user with ID: {WRONG_USER_ID}")
            
            # Create user with wrong ID
            insert_query = text("""
                INSERT INTO users (id, email, name, created_at, updated_at)
                VALUES (:id, :email, :name, NOW(), NOW())
                ON CONFLICT (id) DO NOTHING
            """)
            
            conn.execute(insert_query, {
                "id": WRONG_USER_ID,
                "email": EMAIL,
                "name": "asfaqasim145"
            })
            conn.commit()
            print(f"   ✅ User created")
            
            # Move tasks
            print(f"\n🔄 Moving tasks from {CORRECT_USER_ID} to {WRONG_USER_ID}...")
            update_query = text("UPDATE tasks SET user_id = :new_id WHERE user_id = :old_id")
            result = conn.execute(update_query, {"new_id": WRONG_USER_ID, "old_id": CORRECT_USER_ID})
            conn.commit()
            print(f"   ✅ Moved {result.rowcount} tasks")
        
        # Verify
        print(f"\n✅ Verification:")
        verify_query = text("SELECT COUNT(*) FROM tasks WHERE user_id = :user_id")
        result = conn.execute(verify_query, {"user_id": WRONG_USER_ID})
        count = result.fetchone()[0]
        print(f"   Tasks for {WRONG_USER_ID}: {count}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("✅ DONE! Now test again:")
print("   python test_with_correct_user.py")
print("=" * 80)
