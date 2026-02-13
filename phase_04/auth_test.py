#!/usr/bin/env python3
"""Test the authentication and task retrieval flow."""

import os
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))
sys.path.insert(0, str(backend_path / "src"))

# Change to backend directory so config can be imported
original_cwd = os.getcwd()
os.chdir(str(backend_path))

from src.db import engine, init_db
from src.models.base_models import Task, User, TaskStatus
from sqlmodel import Session, select
from src.services.auth_service import create_access_token, verify_token
from fastapi import HTTPException

def test_auth_flow():
    """Test the authentication flow and token verification."""
    print("=" * 80)
    print("AUTHENTICATION FLOW TEST")
    print("=" * 80)
    
    try:
        # Initialize database
        init_db()
        print("Database initialized successfully")
        
        # Create a test user
        with Session(engine) as session:
            # Check if test user already exists
            test_user = session.exec(select(User).where(User.email == "test@example.com")).first()
            
            if not test_user:
                # Create a new test user
                test_user = User(email="test@example.com", name="Test User")
                session.add(test_user)
                session.commit()
                session.refresh(test_user)
                print(f"Created test user: {test_user.email} (ID: {test_user.id})")
            else:
                print(f"Found existing test user: {test_user.email} (ID: {test_user.id})")
        
        # Create a token for the test user
        token_payload = {
            "sub": str(test_user.id),
            "email": test_user.email,
            "name": test_user.name
        }
        token = create_access_token(token_payload)
        print(f"Generated token: {token[:30]}...")
        
        # Verify the token
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials"
        )
        
        try:
            token_data = verify_token(token, credentials_exception)
            print(f"Token verification successful!")
            print(f"User ID from token: {token_data.user_id}")
            print(f"Email from token: {token_data.email}")
        except Exception as e:
            print(f"Token verification failed: {e}")
            import traceback
            traceback.print_exc()
        
        # Test retrieving tasks using the same logic as the API
        print("\nTesting task retrieval with user from token...")
        with Session(engine) as session:
            # Simulate getting user from token (like in tasks_simple.py)
            user_from_token = session.exec(select(User).where(User.id == test_user.id)).first()
            
            if user_from_token:
                print(f"Found user from token: {user_from_token.email}")
                
                # Get tasks for this user
                tasks = session.exec(select(Task).where(Task.user_id == str(user_from_token.id))).all()
                print(f"Found {len(tasks)} tasks for user")
                
                for i, task in enumerate(tasks):
                    print(f"  {i+1}. {task.title} - Status: {task.status}")
            else:
                print("Could not find user from token")
        
    except Exception as e:
        print(f"Authentication flow test failed: {e}")
        import traceback
        traceback.print_exc()


def test_get_user_from_token_function():
    """Test the get_user_from_token function from tasks_simple.py directly."""
    print("\n" + "=" * 80)
    print("GET_USER_FROM_TOKEN FUNCTION TEST")
    print("=" * 80)
    
    try:
        # Initialize database
        init_db()
        
        # Create a test user
        with Session(engine) as session:
            # Check if test user already exists
            test_user = session.exec(select(User).where(User.email == "get_user_test@example.com")).first()
            
            if not test_user:
                # Create a new test user
                test_user = User(email="get_user_test@example.com", name="Get User Test")
                session.add(test_user)
                session.commit()
                session.refresh(test_user)
                print(f"Created test user: {test_user.email} (ID: {test_user.id})")
            else:
                print(f"Found existing test user: {test_user.email} (ID: {test_user.id})")
        
        # Create a token
        token_payload = {
            "sub": str(test_user.id),
            "email": test_user.email,
            "name": test_user.name
        }
        token = create_access_token(token_payload)
        print(f"Generated token for test: {token[:30]}...")
        
        # Now test the function from tasks_simple.py by importing it
        from src.api.routes.tasks_simple import get_user_from_token
        from fastapi import Header
        from contextlib import contextmanager
        
        # Mock the database session dependency
        @contextmanager
        def mock_db_session():
            session = Session(engine)
            try:
                yield session
            finally:
                session.close()
        
        # Test the function
        try:
            # Create a mock header
            mock_authorization = f"Bearer {token}"
            
            # Call the function directly
            with mock_db_session() as session:
                user = get_user_from_token(mock_authorization, session)
                print(f"Successfully got user from token: {user.email}")
                
                # Test task retrieval like in the list_tasks function
                tasks_query = select(Task).where(Task.user_id == str(user.id))
                tasks = session.exec(tasks_query).all()
                
                print(f"Found {len(tasks)} tasks for user via get_user_from_token")
                for i, task in enumerate(tasks):
                    print(f"  {i+1}. {task.title} - Status: {task.status}")
                    
        except Exception as e:
            print(f"get_user_from_token function test failed: {e}")
            import traceback
            traceback.print_exc()
    
    except Exception as e:
        print(f"Get user from token test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_auth_flow()
    test_get_user_from_token_function()
    
    # Change back to original directory
    os.chdir(original_cwd)