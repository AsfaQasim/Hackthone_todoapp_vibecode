#!/usr/bin/env python3
"""
Debug script to test the chat endpoint and understand the 401 error
"""

import requests
import jwt
import uuid
import os
from dotenv import load_dotenv
import sys
from datetime import datetime, timedelta
# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.base_models import User

load_dotenv()

# JWT configuration (should match backend config)
# Load from the same place as the backend
try:
    # Try to load the same way the backend does
    from backend.src.services.auth_service import SECRET_KEY, ALGORITHM
    print(f"Using SECRET_KEY from backend: {SECRET_KEY[:10]}..." if SECRET_KEY else "SECRET_KEY is not set")
except ImportError:
    # Fallback to environment variable
    SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "your-secret-key-change-in-production")
    ALGORITHM = "HS256"
    print(f"Using SECRET_KEY from env: {SECRET_KEY[:10]}..." if SECRET_KEY else "SECRET_KEY is not set")

def decode_token_debug(token):
    """Decode token without verification to see its contents"""
    try:
        # Decode without verification to inspect payload
        payload = jwt.decode(token, options={"verify_signature": False}, algorithms=[ALGORITHM])
        print(f"Token payload: {payload}")
        return payload
    except Exception as e:
        print(f"Error decoding token: {e}")
        return None

def get_first_user():
    """Get the first user from the database to use for testing"""
    try:
        # Import the database setup from the backend
        from backend.src.db import SessionLocal
        db = SessionLocal()

        user = db.query(User).first()
        if user:
            print(f"Found user in DB: {user.id} (type: {type(user.id)})")
            # Convert to string to see format
            user_id_str = str(user.id)
            print(f"User ID as string: {user_id_str}")
            return user_id_str
        else:
            print("No users found in database")
            return None
    except Exception as e:
        print(f"Error getting user from DB: {e}")
        # Return a known test user ID as fallback
        return "123e4567-e89b-12d3-a456-426614174000"  # Standard UUID format
    finally:
        try:
            db.close()
        except:
            pass

def test_chat_endpoint():
    """Test the chat endpoint with a sample request"""
    
    # Get a real user ID from the database
    user_id = get_first_user()
    if not user_id:
        print("Cannot test without a valid user ID")
        return
    
    print(f"Using user ID: {user_id}")
    
    # Create a test token (this mimics what would be in the auth system)
    token_data = {
        "user_id": user_id,  # Use the actual user ID from DB
        "email": "test@example.com",
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    
    print(f"Generated test token: {token[:20]}...")
    decode_token_debug(token)
    
    # Prepare the request
    url = f"http://localhost:8000/api/{user_id}/chat"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    data = {
        "message": "Hello, how are you?",
        "conversation_id": None
    }
    
    print(f"\nMaking request to: {url}")
    print(f"Headers: {headers}")
    print(f"Data: {data}")
    
    try:
        response = requests.post(url, json=data, headers=headers)
        print(f"\nResponse Status: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        if response.status_code == 401:
            print("\nThe request failed with 401 Unauthorized")
            print("This could be due to:")
            print("1. Invalid token format")
            print("2. Expired token")
            print("3. User ID mismatch between token and path")
            print("4. User not found in database")
            print("5. UUID format mismatch")
        else:
            print("\nRequest succeeded!")
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the backend server.")
        print("Make sure the backend server is running on http://localhost:8000")
    except Exception as e:
        print(f"Error making request: {e}")

if __name__ == "__main__":
    print("Debugging the chat endpoint 401 error...")
    test_chat_endpoint()