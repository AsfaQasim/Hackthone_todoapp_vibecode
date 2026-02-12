import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
FRONTEND_BASE_URL = "http://localhost:3000"

def test_api_endpoints():
    print("Testing Todo API endpoints...")
    
    # Test health endpoint
    print("\n1. Testing health endpoint:")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Error connecting to backend: {e}")
        print("Make sure the FastAPI server is running on port 8000")
        return

    # Test unauthorized access to protected endpoints
    print("\n2. Testing unauthorized access to protected endpoints:")
    try:
        response = requests.get(f"{BASE_URL}/todos/")
        print(f"Unauthorized access attempt: {response.status_code}")
        if response.status_code == 401:
            print("✓ Correctly rejected unauthorized request")
        else:
            print("✗ Failed to reject unauthorized request")
    except Exception as e:
        print(f"Error testing unauthorized access: {e}")

    print("\n3. Manual testing instructions:")
    print("   To fully test the authentication flow, you need to:")
    print("   a) Start the Next.js frontend: cd frontend && npm run dev")
    print("   b) Start the FastAPI backend: cd backend && python main.py") 
    print("   c) Open browser to http://localhost:3000")
    print("   d) Create an account and sign in")
    print("   e) Create some todos")
    print("   f) Verify that you can only see your own todos")
    print("   g) Try signing in with another account to verify isolation")

    print("\n4. API endpoints available:")
    print("   GET    /health                    - Health check")
    print("   GET    /todos/                    - Get user's todos (requires auth)")
    print("   POST   /todos/                    - Create new todo (requires auth)")
    print("   GET    /todos/{id}                - Get specific todo (requires auth)")
    print("   PUT    /todos/{id}                - Update specific todo (requires auth)")
    print("   DELETE /todos/{id}                - Delete specific todo (requires auth)")
    print("   GET    /todos/count               - Get user's todo count (requires auth)")
    print("   DELETE /todos/                    - Delete all user's todos (requires auth)")

    print("\n5. Headers required for authenticated requests:")
    print("   Authorization: Bearer <JWT_TOKEN>")
    print("   Content-Type: application/json")

if __name__ == "__main__":
    test_api_endpoints()