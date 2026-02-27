"""Check backend database and models"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

print("Loading environment...")
from dotenv import load_dotenv
load_dotenv('backend/.env')

print(f"DATABASE_URL: {os.getenv('DATABASE_URL')[:50]}...")

print("\nImporting config...")
from config import settings
print(f"Settings database_url: {settings.database_url[:80]}...")

print("\nImporting db...")
from src.db import engine, DATABASE_URL
print(f"Engine URL: {str(engine.url)[:80]}...")

print("\nImporting models...")
from src.models.base_models import User, Task

print("\nTrying to query database...")
from sqlmodel import Session, select

try:
    with Session(engine) as session:
        # Try to query users
        statement = select(User)
        users = session.exec(statement).all()
        print(f"✅ Found {len(users)} users in database")
        for user in users[:3]:
            print(f"  - {user.email} (ID: {user.id})")
except Exception as e:
    print(f"❌ Database query error: {e}")
    import traceback
    traceback.print_exc()

print("\nTrying to create a test user...")
try:
    with Session(engine) as session:
        import uuid
        test_user = User(
            id=uuid.uuid4(),
            email="test@test.com",
            name="Test User"
        )
        
        # Check if user already exists
        existing = session.exec(select(User).where(User.email == "test@test.com")).first()
        if existing:
            print(f"✅ User already exists: {existing.email} (ID: {existing.id})")
        else:
            session.add(test_user)
            session.commit()
            print(f"✅ Created test user: {test_user.email} (ID: {test_user.id})")
except Exception as e:
    print(f"❌ User creation error: {e}")
    import traceback
    traceback.print_exc()
