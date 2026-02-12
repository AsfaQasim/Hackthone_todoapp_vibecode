#!/usr/bin/env python3
"""
Test script to verify token verification process
"""

import os
import sys
from datetime import datetime, timedelta
import jwt
import uuid

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from dotenv import load_dotenv
load_dotenv()

# Import backend components
from backend.src.services.auth_service import verify_token, SECRET_KEY, ALGORITHM
from backend.src.db import SessionLocal
from backend.src.models.base_models import User

def test_token_verification():
    """Test the token verification process step by step"""
    
    # Get a real user from the database
    db = SessionLocal()
    try:
        user = db.query(User).first()
        if not user:
            print("No users found in database")
            return
            
        print(f"Found user: {user.id} (type: {type(user.id)})")
        print(f"User ID as string: {str(user.id)}")
        
        # Create a token with the actual user ID
        token_data = {
            "user_id": str(user.id),  # Use the actual user ID from the database
            "email": user.email,
            "exp": datetime.utcnow() + timedelta(hours=1)
        }
        
        # Encode the token using the same method as the auth service
        from backend.src.services.auth_service import create_access_token
        token = create_access_token(data=token_data)
        
        print(f"Created token: {token[:30]}...")
        
        # Now try to verify the token
        credentials_exception = Exception("Could not validate credentials")
        try:
            token_data_verified = verify_token(token, credentials_exception)
            print(f"Token verification successful: {token_data_verified}")
            
            # Now try to find the user in the database using the verified token data
            verified_user_id = token_data_verified.user_id
            print(f"Verified user ID: {verified_user_id} (type: {type(verified_user_id)})")
            
            # Try to find user with the verified ID
            found_user = db.query(User).filter(User.id == verified_user_id).first()
            if found_user:
                print(f"Found user in DB using verified ID: {found_user.id}")
            else:
                print(f"Could NOT find user in DB using verified ID: {verified_user_id}")
                
                # Try with hex format
                try:
                    uuid_obj = uuid.UUID(verified_user_id)
                    hex_uuid = uuid_obj.hex
                    found_user_hex = db.query(User).filter(User.id == hex_uuid).first()
                    if found_user_hex:
                        print(f"Found user in DB using hex format: {found_user_hex.id}")
                        print(f"DB user ID (raw): {repr(found_user_hex.id)}")
                        print(f"DB user ID (str): {str(found_user_hex.id)}")
                        print(f"DB user ID (hex): {uuid.UUID(str(found_user_hex.id)).hex}")
                    else:
                        print(f"Could NOT find user in DB using hex format: {hex_uuid}")
                        
                        # Try the original user ID in hex format
                        orig_user_hex = uuid.UUID(str(user.id)).hex
                        found_orig_hex = db.query(User).filter(User.id == orig_user_hex).first()
                        if found_orig_hex:
                            print(f"Original user ID in hex format works: {orig_user_hex}")
                        else:
                            print(f"Even original user ID in hex doesn't work")
                            
                except Exception as e:
                    print(f"Error converting to UUID: {e}")
                    
        except Exception as e:
            print(f"Token verification failed: {e}")
            
    except Exception as e:
        print(f"Error in test: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("Testing token verification process...")
    test_token_verification()