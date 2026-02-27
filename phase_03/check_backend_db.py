"""Quick check of backend database configuration"""
import os
import sys

# Add backend to path
sys.path.insert(0, 'backend')
sys.path.insert(0, 'backend/src')

print("=" * 60)
print("Backend Database Configuration Check")
print("=" * 60)

# Load environment
from dotenv import load_dotenv
load_dotenv('backend/.env')

print("\n1. Environment Variables:")
print(f"   DATABASE_URL: {os.getenv('DATABASE_URL', 'NOT SET')[:50]}...")
print(f"   ENVIRONMENT: {os.getenv('ENVIRONMENT', 'NOT SET')}")
print(f"   BETTER_AUTH_SECRET: {'SET' if os.getenv('BETTER_AUTH_SECRET') else 'NOT SET'}")

print("\n2. Config Module:")
try:
    from config import settings
    print(f"   ✅ Config loaded")
    print(f"   Database URL from config: {settings.database_url[:50]}...")
    
    if 'sqlite' in settings.database_url.lower():
        print("   ⚠️  WARNING: Using SQLite!")
    elif 'postgresql' in settings.database_url.lower() or 'neon' in settings.database_url.lower():
        print("   ✅ Using PostgreSQL (Neon)")
    else:
        print(f"   ❓ Unknown database type")
        
except Exception as e:
    print(f"   ❌ Error loading config: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n3. Database Connection:")
try:
    from src.db import engine
    print(f"   Engine URL: {str(engine.url)[:50]}...")
    
    if 'sqlite' in str(engine.url).lower():
        print("   ⚠️  WARNING: Engine using SQLite!")
    elif 'postgresql' in str(engine.url).lower():
        print("   ✅ Engine using PostgreSQL")
    
    # Try to connect
    with engine.connect() as conn:
        result = conn.execute("SELECT 1")
        print("   ✅ Connection successful!")
        
except Exception as e:
    print(f"   ❌ Connection failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n4. Check User Table:")
try:
    from sqlalchemy import inspect, text
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"   Tables found: {tables}")
    
    if 'user' in tables:
        print("   ✅ User table exists")
        
        # Count users
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM \"user\""))
            count = result.scalar()
            print(f"   Users in database: {count}")
    else:
        print("   ⚠️  User table missing!")
        print("   Run: python -c 'from backend.src.db import init_db; init_db()'")
        
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("Check complete!")
print("=" * 60)
