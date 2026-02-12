import os
import sys
import uuid
from datetime import datetime

# Add the backend/src directory to the path so imports work correctly
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))
sys.path.insert(0, os.path.join(os.getcwd(), 'backend', 'src'))

# Import the settings to see what database URL is being used
from config import settings
print(f"Database URL being used: {settings.database_url}")

from db import SessionLocal, engine
from models.base_models import Base, User

def create_test_user():
    # Create the tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Create a new session
    db = SessionLocal()
    
    try:
        # Create a test user with a unique email
        test_user = User(
            id=uuid.uuid4(),  # Generate a new UUID
            email=f"test_{uuid.uuid4()}@example.com",  # Unique email
            name="Test User"
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print(f"Created test user with ID: {test_user.id}")
        print(f"Email: {test_user.email}")
        print(f"Name: {test_user.name}")
        
        # Query the user back to verify it was saved
        saved_user = db.query(User).filter(User.id == test_user.id).first()
        if saved_user:
            print(f"Verified user exists in session: {saved_user.email}")
        else:
            print("User not found in current session!")
        
        return test_user
    except Exception as e:
        print(f"Error creating test user: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    user = create_test_user()