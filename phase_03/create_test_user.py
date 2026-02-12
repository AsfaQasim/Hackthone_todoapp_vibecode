import os
import sys
import uuid
from datetime import datetime

# Add the backend/src directory to the path so imports work correctly
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))
sys.path.insert(0, os.path.join(os.getcwd(), 'backend', 'src'))

import config
from db import SessionLocal, engine
from models.base_models import Base, User

def create_test_user():
    # Create the tables if they don't exist
    Base.metadata.create_all(bind=engine)

    # Create a new session
    db = SessionLocal()

    try:
        # Create a test user
        test_user = User(
            id=uuid.uuid4(),  # Generate a new UUID
            email="test@example.com",
            name="Test User"
        )

        db.add(test_user)
        db.commit()
        db.refresh(test_user)

        print(f"Created test user with ID: {test_user.id}")
        print(f"Email: {test_user.email}")
        print(f"Name: {test_user.name}")

        return test_user
    except Exception as e:
        print(f"Error creating test user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    user = create_test_user()