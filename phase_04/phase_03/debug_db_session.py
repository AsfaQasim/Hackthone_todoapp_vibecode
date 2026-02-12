import os
import sys

# Add the backend/src directory to the path so imports work correctly
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))
sys.path.insert(0, os.path.join(os.getcwd(), 'backend', 'src'))

from config import settings
from db import SessionLocal, engine
from models.base_models import User
import uuid

print(f"Database URL from settings: {settings.database_url}")

# Create a new session
db = SessionLocal()
try:
    # Query for the specific user that we know exists
    user_id = "776e40cf-6874-43a2-bb12-b43f117df73c"
    
    # First, try with the canonical format (with dashes)
    user_canonical = db.query(User).filter(User.id == user_id).first()
    print(f"User with canonical format found: {user_canonical is not None}")
    
    # Convert to hex format and try again
    hex_uuid = uuid.UUID(user_id).hex
    print(f"Converted hex UUID: {hex_uuid}")
    
    user_hex = db.query(User).filter(User.id == hex_uuid).first()
    print(f"User with hex format found: {user_hex is not None}")
    
    if user_hex:
        print(f"User details: ID={user_hex.id}, Email={user_hex.email}, Name={user_hex.name}")
    
    # Also try querying all users to see what's there
    all_users = db.query(User).all()
    print(f"Total users in database: {len(all_users)}")
    for u in all_users:
        print(f"  - ID: {u.id}, Email: {u.email}, Name: {u.name}")
        
finally:
    db.close()