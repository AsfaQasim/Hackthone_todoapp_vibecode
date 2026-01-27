"""
Script to create a test user in the backend database that matches the frontend user.
This will help synchronize the frontend and backend authentication systems.
"""
import sys
import os
import uuid
import hashlib

# Add the backend source to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from backend.src.models.base_models import User, Base
from backend.src.db import DATABASE_URL, engine, SessionLocal

def create_test_user_in_backend():
    """Create a test user in the backend database with a known UUID."""

    # Use the existing database session
    db = SessionLocal()

    try:
        # Create a test user with a known UUID
        test_user_id = uuid.uuid4()  # This will be converted to hex by the GUID type
        test_email = "test@example.com"
        test_name = "Test User"

        # Check if user already exists
        existing_user = db.query(User).filter(User.email == test_email).first()
        if existing_user:
            print(f"User with email {test_email} already exists with ID: {existing_user.id}")
            return existing_user.id

        # Create new user - the GUID type will handle the conversion
        user = User(
            id=test_user_id,  # Pass the UUID object, GUID type will convert appropriately
            email=test_email,
            name=test_name
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        print(f"Created test user in backend:")
        print(f"  ID: {user.id}")  # This will show the hex representation
        print(f"  Email: {user.email}")
        print(f"  Name: {user.name}")

        return user.id

    except Exception as e:
        print(f"Error creating test user: {e}")
        db.rollback()
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    created_user_id = create_test_user_in_backend()
    print(f"\nUse this user ID for testing: {created_user_id}")
    
    # Also print a sample JWT token for testing
    import jwt
    import os
    from datetime import datetime, timedelta
    
    SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-in-production")
    
    # Create a sample token
    payload = {
        "sub": created_user_id,  # Use the actual user ID from the database
        "email": "test@example.com",
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    print(f"Sample JWT token: {token}")