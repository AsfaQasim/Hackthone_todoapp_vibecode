"""Test backend login endpoint and database connection"""

import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

print("=" * 60)
print("Testing Backend Login")
print("=" * 60)

# Test 1: Check environment variables
print("\n1. Checking environment variables...")
from dotenv import load_dotenv
load_dotenv('backend/.env')

DATABASE_URL = os.getenv('DATABASE_URL')
BETTER_AUTH_SECRET = os.getenv('BETTER_AUTH_SECRET')

print(f"   DATABASE_URL: {'✅ Set' if DATABASE_URL else '❌ Missing'}")
print(f"   BETTER_AUTH_SECRET: {'✅ Set' if BETTER_AUTH_SECRET else '❌ Missing'}")

if not DATABASE_URL:
    print("\n❌ DATABASE_URL is missing!")
    sys.exit(1)

# Test 2: Check database connection
print("\n2. Testing database connection...")
try:
    from src.db import engine
    with engine.connect() as conn:
        print("   ✅ Database connection successful!")
except Exception as e:
    print(f"   ❌ Database connection failed: {e}")
    print("\n   Possible issues:")
    print("   - Database server is down")
    print("   - Wrong credentials in DATABASE_URL")
    print("   - Network/firewall blocking connection")
    sys.exit(1)

# Test 3: Check if User table exists
print("\n3. Checking database tables...")
try:
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"   Found tables: {tables}")
    
    if 'user' in tables:
        print("   ✅ User table exists")
    else:
        print("   ⚠️  User table missing, creating...")
        from src.db import init_db
        init_db()
        print("   ✅ Tables created")
except Exception as e:
    print(f"   ❌ Error checking tables: {e}")
    sys.exit(1)

# Test 4: Test login function
print("\n4. Testing login function...")
try:
    from routes.auth import login, LoginRequest
    from src.db import get_db
    
    # Create a test request
    login_request = LoginRequest(
        email="test@test.com",
        password="test123"
    )
    
    # Get database session
    db = next(get_db())
    
    # Try login
    result = login(login_request, db)
    print(f"   ✅ Login function works!")
    print(f"   Token: {result.access_token[:20]}...")
    print(f"   User ID: {result.user_id}")
    
except Exception as e:
    print(f"   ❌ Login function failed: {e}")
    import traceback
    print("\n   Full error:")
    print(traceback.format_exc())
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ All tests passed! Backend should work.")
print("=" * 60)
