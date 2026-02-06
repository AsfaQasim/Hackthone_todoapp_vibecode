#!/usr/bin/env python3
"""
Comprehensive system diagnostic to check all components
"""
import requests
import json
import sys

def test_component(name, test_func):
    """Test a component and report results"""
    print(f"\n{'='*60}")
    print(f"Testing: {name}")
    print('='*60)
    try:
        result = test_func()
        if result:
            print(f"✅ {name}: PASSED")
            return True
        else:
            print(f"❌ {name}: FAILED")
            return False
    except Exception as e:
        print(f"❌ {name}: ERROR - {e}")
        return False

def test_backend_health():
    """Test backend health endpoint"""
    response = requests.get("http://localhost:8000/health", timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 200

def test_backend_auth():
    """Test backend authentication"""
    response = requests.post(
        "http://localhost:8000/login",
        json={"email": "test@example.com", "password": "test123"},
        timeout=5
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Token received: {data.get('access_token', 'None')[:30]}...")
        return True
    return False

def test_backend_tasks():
    """Test backend tasks endpoint"""
    # First login
    login_response = requests.post(
        "http://localhost:8000/login",
        json={"email": "asfaqasim145@gmail.com", "password": "test123"}
    )
    
    if login_response.status_code != 200:
        print("Login failed, trying register...")
        login_response = requests.post(
            "http://localhost:8000/register",
            json={"email": "asfaqasim145@gmail.com", "password": "test123"}
        )
    
    if login_response.status_code != 200:
        print(f"Auth failed: {login_response.text}")
        return False
    
    token = login_response.json()["access_token"]
    
    # Test tasks endpoint
    tasks_response = requests.get(
        "http://localhost:8000/api/tasks",
        headers={"Authorization": f"Bearer {token}"},
        timeout=5
    )
    
    print(f"Status: {tasks_response.status_code}")
    if tasks_response.status_code == 200:
        tasks = tasks_response.json()
        print(f"Tasks found: {len(tasks)}")
        return True
    else:
        print(f"Error: {tasks_response.text}")
        return False

def test_frontend():
    """Test frontend is running"""
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        print(f"Status: {response.status_code}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        print("Frontend not running on port 3000")
        return False

def test_frontend_api():
    """Test frontend API routes"""
    try:
        # Test with a simple GET to see if API routes are accessible
        response = requests.get("http://localhost:3000/api/session", timeout=5)
        print(f"Status: {response.status_code}")
        return response.status_code in [200, 401]  # Either is fine, means API is working
    except requests.exceptions.ConnectionError:
        print("Frontend API not accessible")
        return False

def main():
    """Run all diagnostic tests"""
    print("\n" + "="*60)
    print("SYSTEM DIAGNOSTIC")
    print("="*60)
    
    results = {}
    
    # Test backend components
    results['Backend Health'] = test_component('Backend Health', test_backend_health)
    results['Backend Auth'] = test_component('Backend Authentication', test_backend_auth)
    results['Backend Tasks'] = test_component('Backend Tasks API', test_backend_tasks)
    
    # Test frontend components
    results['Frontend'] = test_component('Frontend Server', test_frontend)
    results['Frontend API'] = test_component('Frontend API Routes', test_frontend_api)
    
    # Summary
    print("\n" + "="*60)
    print("DIAGNOSTIC SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All systems operational!")
    else:
        print("\n⚠️  Some components need attention")
        
        # Provide specific guidance
        if not results['Backend Health']:
            print("\n❌ Backend is not running. Start it with:")
            print("   cd backend && python main.py")
        
        if not results['Frontend']:
            print("\n❌ Frontend is not running. Start it with:")
            print("   cd frontend && npm run dev")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
