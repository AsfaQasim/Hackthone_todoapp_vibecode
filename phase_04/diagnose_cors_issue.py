"""Comprehensive CORS and backend connectivity diagnosis."""
import requests
import json

print("="*70)
print("BACKEND CONNECTIVITY & CORS DIAGNOSIS")
print("="*70)

# Test 1: Backend health check
print("\n1. Testing backend health endpoint...")
try:
    response = requests.get("http://localhost:8000/health", timeout=5)
    print(f"   ✅ Backend is running!")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
except requests.exceptions.ConnectionError:
    print(f"   ❌ Backend is NOT running on http://localhost:8000")
    print(f"   Please start backend: cd backend && python main.py")
    exit(1)
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Test 2: CORS preflight (OPTIONS)
print("\n2. Testing CORS preflight (OPTIONS) for /api/tasks...")
try:
    response = requests.options(
        "http://localhost:8000/api/tasks",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "authorization,content-type"
        },
        timeout=5
    )
    print(f"   Status: {response.status_code}")
    
    cors_headers = {
        k: v for k, v in response.headers.items() 
        if k.lower().startswith('access-control')
    }
    
    if cors_headers:
        print(f"   ✅ CORS headers present:")
        for k, v in cors_headers.items():
            print(f"      {k}: {v}")
    else:
        print(f"   ❌ No CORS headers found!")
        print(f"   All headers: {dict(response.headers)}")
        
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Actual GET request with CORS
print("\n3. Testing GET /api/tasks with CORS headers...")
try:
    response = requests.get(
        "http://localhost:8000/api/tasks",
        headers={
            "Origin": "http://localhost:3000",
        },
        timeout=5
    )
    print(f"   Status: {response.status_code}")
    
    cors_headers = {
        k: v for k, v in response.headers.items() 
        if k.lower().startswith('access-control')
    }
    
    if cors_headers:
        print(f"   ✅ CORS headers present:")
        for k, v in cors_headers.items():
            print(f"      {k}: {v}")
    else:
        print(f"   ❌ No CORS headers found!")
        
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Check backend environment
print("\n4. Checking backend configuration...")
try:
    with open('backend/.env', 'r') as f:
        env_content = f.read()
        if 'ALLOWED_ORIGINS' in env_content:
            for line in env_content.split('\n'):
                if line.startswith('ALLOWED_ORIGINS'):
                    print(f"   ✅ {line}")
        else:
            print(f"   ⚠️  ALLOWED_ORIGINS not found in .env")
except Exception as e:
    print(f"   ❌ Error reading .env: {e}")

# Test 5: Test frontend API route
print("\n5. Testing frontend API proxy (if running)...")
try:
    response = requests.get(
        "http://localhost:3000/api/health",
        timeout=5
    )
    print(f"   ✅ Frontend is running!")
    print(f"   Status: {response.status_code}")
except requests.exceptions.ConnectionError:
    print(f"   ⚠️  Frontend is NOT running on http://localhost:3000")
    print(f"   Start frontend: cd frontend && npm run dev")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "="*70)
print("DIAGNOSIS COMPLETE")
print("="*70)
print("\nIf backend is running but CORS headers are missing:")
print("1. Make sure you restarted backend after CORS fix")
print("2. Check backend console for any errors")
print("3. Run: RESTART_BACKEND_CORS_FIX.bat")
print("\nIf frontend shows CORS error:")
print("1. Open browser DevTools > Network tab")
print("2. Look for failed request")
print("3. Check if it's calling /api/tasks (Next.js) or localhost:8000 (direct)")
print("4. If calling localhost:8000 directly, that's the issue!")
