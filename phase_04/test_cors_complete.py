"""Complete CORS diagnostic test."""
import requests
import json

BACKEND_URL = "http://localhost:8000"

def test_cors():
    """Test CORS configuration."""
    print("=" * 60)
    print("CORS DIAGNOSTIC TEST")
    print("=" * 60)
    print()
    
    # Test 1: Health check
    print("Test 1: Backend Health Check")
    print("-" * 60)
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        print(f"✓ Status: {response.status_code}")
        print(f"✓ Response: {response.json()}")
        print(f"✓ CORS Headers:")
        for header, value in response.headers.items():
            if 'access-control' in header.lower() or 'origin' in header.lower():
                print(f"  - {header}: {value}")
    except requests.exceptions.ConnectionError:
        print("✗ ERROR: Cannot connect to backend!")
        print("  Backend is not running on http://localhost:8000")
        print("  Run: FIX_CORS_COMPLETE.bat")
        return False
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False
    
    print()
    
    # Test 2: OPTIONS preflight request
    print("Test 2: OPTIONS Preflight Request")
    print("-" * 60)
    try:
        headers = {
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'POST',
            'Access-Control-Request-Headers': 'content-type,authorization'
        }
        response = requests.options(f"{BACKEND_URL}/api/chat", headers=headers, timeout=5)
        print(f"✓ Status: {response.status_code}")
        print(f"✓ CORS Headers:")
        for header, value in response.headers.items():
            if 'access-control' in header.lower():
                print(f"  - {header}: {value}")
        
        # Check required headers
        required_headers = [
            'access-control-allow-origin',
            'access-control-allow-methods',
            'access-control-allow-headers'
        ]
        missing = []
        for h in required_headers:
            if h not in [k.lower() for k in response.headers.keys()]:
                missing.append(h)
        
        if missing:
            print(f"✗ Missing CORS headers: {missing}")
            return False
        else:
            print("✓ All required CORS headers present")
            
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False
    
    print()
    
    # Test 3: Actual POST request with Origin
    print("Test 3: POST Request with Origin Header")
    print("-" * 60)
    try:
        headers = {
            'Origin': 'http://localhost:3000',
            'Content-Type': 'application/json'
        }
        data = {
            "message": "test",
            "user_id": "test-user"
        }
        response = requests.post(
            f"{BACKEND_URL}/api/chat",
            headers=headers,
            json=data,
            timeout=5
        )
        print(f"✓ Status: {response.status_code}")
        print(f"✓ CORS Headers:")
        for header, value in response.headers.items():
            if 'access-control' in header.lower():
                print(f"  - {header}: {value}")
                
        # Check if Access-Control-Allow-Origin is present
        if 'access-control-allow-origin' in [k.lower() for k in response.headers.keys()]:
            print("✓ Access-Control-Allow-Origin header is present")
        else:
            print("✗ Access-Control-Allow-Origin header is MISSING")
            return False
            
    except Exception as e:
        print(f"✗ ERROR: {e}")
        return False
    
    print()
    print("=" * 60)
    print("✓ ALL CORS TESTS PASSED!")
    print("=" * 60)
    print()
    print("Your backend CORS is configured correctly.")
    print("If you still see CORS errors in browser:")
    print("1. Clear browser cache (Ctrl+Shift+Delete)")
    print("2. Hard refresh (Ctrl+F5)")
    print("3. Check browser console for actual error")
    print("4. Verify frontend is using: http://localhost:8000")
    return True

if __name__ == "__main__":
    test_cors()
