"""Create user and sample tasks in database"""
import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://neondb_owner:npg_6DzBwoCp1Muf@ep-holy-flower-ahrkffp6-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require')

USER_EMAIL = "asfaqasim145@gmail.com"
USER_ID = "add60fd1-792f-4ab9-9a53-e2f859482c59"

print("=" * 80)
print("🔧 CREATING USER AND TASKS")
print("=" * 80)

try:
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # Create user
        print(f"\n1️⃣ Creating user: {USER_EMAIL}")
        user_query = text('''
            INSERT INTO "user" (id, email, name, password, created_at, updated_at)
            VALUES (:id, :email, :name, :password, NOW(), NOW())
            ON CONFLICT (id) DO UPDATE SET email = :email
        ''')
        
        conn.execute(user_query, {
            "id": USER_ID,
            "email": USER_EMAIL,
            "name": "asfaqasim145",
            "password": "dummy_password_hash"  # Not used for auth
        })
        conn.commit()
        print(f"   ✅ User created/updated")
        
        # Create sample tasks
        print(f"\n2️⃣ Creating sample tasks...")
        tasks = [
            ("eating", "Created via AI Assistant"),
            ("playing games", "Created via AI Assistant"),
            ("studying", "Created via AI Assistant"),
        ]
        
        for title, desc in tasks:
            task_query = text('''
                INSERT INTO task (id, title, description, completed, user_id, created_at, updated_at)
                VALUES (gen_random_uuid(), :title, :description, false, :user_id, NOW(), NOW())
            ''')
            
            conn.execute(task_query, {
                "title": title,
                "description": desc,
                "user_id": USER_ID
            })
        
        conn.commit()
        print(f"   ✅ Created {len(tasks)} tasks")
        
        # Verify
        print(f"\n3️⃣ Verifying...")
        verify_query = text('SELECT COUNT(*) FROM task WHERE user_id = :user_id')
        result = conn.execute(verify_query, {"user_id": USER_ID})
        count = result.fetchone()[0]
        print(f"   ✅ Total tasks for user: {count}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("✅ DONE! Now test:")
print("   python -c \"import requests; r = requests.get('http://localhost:8000/api/my-tasks'); print(r.json())\"")
print("=" * 80)
