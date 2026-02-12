"""
End-to-End Flow Verification for Better Auth Integration
This script verifies the complete flow: Sign-up -> JWT generation -> API call with Bearer token -> Backend validation -> Data return
"""

import requests
import json
from datetime import datetime
import os

# Configuration
BASE_URL = os.getenv("API_URL", "http://localhost:8000")
FRONTEND_BASE_URL = os.getenv("NEXT_PUBLIC_BETTER_AUTH_URL", "http://localhost:3000")

def test_e2e_flow():
    print("Starting End-to-End Flow Verification...")
    
    # Step 1: Sign-up a new user
    print("\n1. Testing user sign-up...")
    signup_data = {
        "email": f"test_user_{int(datetime.now().timestamp())}@example.com",
        "password": "SecurePassword123!",
        "name": "Test User"
    }
    
    try:
        signup_response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
        print(f"Sign-up response status: {signup_response.status_code}")
        
        if signup_response.status_code == 200:
            signup_result = signup_response.json()
            print(f"Sign-up successful: {signup_result.get('user', {}).get('email', 'Unknown')}")
            
            # Step 2: Login to get JWT token
            print("\n2. Testing user login to get JWT token...")
            login_data = {
                "email": signup_data["email"],
                "password": signup_data["password"]
            }
            
            login_response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
            print(f"Login response status: {login_response.status_code}")
            
            if login_response.status_code == 200:
                login_result = login_response.json()
                token = login_result.get("token")
                
                if token:
                    print("JWT token received successfully")
                    
                    # Step 3: Make API call with Bearer token
                    print("\n3. Testing API call with Bearer token...")
                    headers = {
                        "Authorization": f"Bearer {token}",
                        "Content-Type": "application/json"
                    }
                    
                    # Test profile endpoint
                    profile_response = requests.get(f"{BASE_URL}/profile", headers=headers)
                    print(f"Profile endpoint response status: {profile_response.status_code}")
                    
                    if profile_response.status_code == 200:
                        profile_data = profile_response.json()
                        print(f"Profile access successful: {profile_data.get('email', 'Unknown')}")
                        
                        # Step 4: Test creating a todo
                        print("\n4. Testing creating a todo...")
                        todo_data = {
                            "title": "Test Todo",
                            "description": "This is a test todo created during E2E flow verification",
                            "completed": False
                        }
                        
                        todo_response = requests.post(f"{BASE_URL}/todos", json=todo_data, headers=headers)
                        print(f"Create todo response status: {todo_response.status_code}")
                        
                        if todo_response.status_code == 200:
                            todo_result = todo_response.json()
                            todo_id = todo_result.get("id")
                            print(f"Todo created successfully with ID: {todo_id}")
                            
                            # Step 5: Test getting the created todo
                            print("\n5. Testing retrieving the created todo...")
                            get_todo_response = requests.get(f"{BASE_URL}/todos/{todo_id}", headers=headers)
                            print(f"Get todo response status: {get_todo_response.status_code}")
                            
                            if get_todo_response.status_code == 200:
                                retrieved_todo = get_todo_response.json()
                                print(f"Successfully retrieved todo: {retrieved_todo.get('title', 'Unknown')}")
                                
                                print("\n✅ End-to-End Flow Verification PASSED!")
                                return True
                            else:
                                print(f"❌ Failed to retrieve todo: {get_todo_response.status_code}")
                        else:
                            print(f"❌ Failed to create todo: {todo_response.status_code}")
                    else:
                        print(f"❌ Profile access failed: {profile_response.status_code}")
                else:
                    print("❌ No token received from login")
            else:
                print(f"❌ Login failed: {login_response.status_code}")
        else:
            print(f"❌ Sign-up failed: {signup_response.status_code}")
    except Exception as e:
        print(f"❌ Error during E2E flow: {str(e)}")
    
    print("\n❌ End-to-End Flow Verification FAILED!")
    return False

def test_negative_flow():
    """
    Test negative scenario: Confirm that deleting a todo_id belonging to "User B" 
    while logged in as "User A" returns a 403 Forbidden via the verify_user_owns_resource dependency.
    """
    print("\n\nTesting Negative Flow (Resource Ownership)...")
    
    # Create two users
    print("Creating two test users...")
    
    # User A
    user_a_data = {
        "email": f"user_a_{int(datetime.now().timestamp())}@example.com",
        "password": "SecurePassword123!",
        "name": "User A"
    }
    
    signup_a_response = requests.post(f"{BASE_URL}/auth/signup", json=user_a_data)
    if signup_a_response.status_code != 200:
        print(f"❌ Failed to create User A: {signup_a_response.status_code}")
        return False
    
    # User B
    user_b_data = {
        "email": f"user_b_{int(datetime.now().timestamp())}@example.com",
        "password": "SecurePassword123!",
        "name": "User B"
    }
    
    signup_b_response = requests.post(f"{BASE_URL}/auth/signup", json=user_b_data)
    if signup_b_response.status_code != 200:
        print(f"❌ Failed to create User B: {signup_b_response.status_code}")
        return False
    
    # Login as User A
    login_a_response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": user_a_data["email"],
        "password": user_a_data["password"]
    })
    
    if login_a_response.status_code != 200:
        print(f"❌ Failed to login as User A: {login_a_response.status_code}")
        return False
    
    token_a = login_a_response.json().get("token")
    if not token_a:
        print("❌ No token for User A")
        return False
    
    # Login as User B
    login_b_response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": user_b_data["email"],
        "password": user_b_data["password"]
    })
    
    if login_b_response.status_code != 200:
        print(f"❌ Failed to login as User B: {login_b_response.status_code}")
        return False
    
    token_b = login_b_response.json().get("token")
    if not token_b:
        print("❌ No token for User B")
        return False
    
    # User A creates a todo
    headers_a = {
        "Authorization": f"Bearer {token_a}",
        "Content-Type": "application/json"
    }
    
    todo_data = {
        "title": "User A's Todo",
        "description": "This todo belongs to User A",
        "completed": False
    }
    
    create_todo_response = requests.post(f"{BASE_URL}/todos", json=todo_data, headers=headers_a)
    if create_todo_response.status_code != 200:
        print(f"❌ Failed to create todo for User A: {create_todo_response.status_code}")
        return False
    
    todo_result = create_todo_response.json()
    todo_id = todo_result.get("id")
    print(f"User A created todo with ID: {todo_id}")
    
    # User B tries to access User A's todo (should fail with 403)
    headers_b = {
        "Authorization": f"Bearer {token_b}",
        "Content-Type": "application/json"
    }
    
    access_todo_response = requests.get(f"{BASE_URL}/todos/{todo_id}", headers=headers_b)
    print(f"User B trying to access User A's todo - Response status: {access_todo_response.status_code}")
    
    if access_todo_response.status_code == 403:
        print("✅ Correctly denied access - User B cannot access User A's todo")
        
        # Try to delete User A's todo as User B (should also fail with 403)
        delete_todo_response = requests.delete(f"{BASE_URL}/todos/{todo_id}", headers=headers_b)
        print(f"User B trying to delete User A's todo - Response status: {delete_todo_response.status_code}")
        
        if delete_todo_response.status_code == 403:
            print("✅ Correctly denied deletion - User B cannot delete User A's todo")
            print("\n✅ Negative Flow (Resource Ownership) Verification PASSED!")
            return True
        else:
            print(f"❌ User B was able to delete User A's todo (status: {delete_todo_response.status_code})")
            return False
    else:
        print(f"❌ User B was able to access User A's todo (status: {access_todo_response.status_code})")
        return False

if __name__ == "__main__":
    print("Running End-to-End Flow Verification Tests...")
    
    # Test positive flow
    e2e_success = test_e2e_flow()
    
    # Test negative flow
    negative_success = test_negative_flow()
    
    if e2e_success and negative_success:
        print("\n🎉 All End-to-End Flow Verification Tests PASSED!")
    else:
        print("\n💥 Some End-to-End Flow Verification Tests FAILED!")