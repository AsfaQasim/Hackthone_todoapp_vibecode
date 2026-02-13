"""Test CORS and backend connection."""
import requests

print("Testing backend connection and CORS...")
print("=" * 70)

# Test 1: Health check
print("\n1. Testing health endpoint...")
try:
    response = requests.get("http://localhost:8000/health")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    print(f"   CORS Headers: {response.headers.get('Access-Control-Allow-Origin', 'NOT SET')}")
except Exception as e:
    print(f"   ERROR: {e}")

# Test 2: Tasks endpoint without auth
print("\n2. Testing tasks endpoint (no auth)...")
try:
    response = requests.get("http://localhost:8000/api/tasks")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    print(f"   CORS Headers: {response.headers.get('Access-Control-Allow-Origin', 'NOT SET')}")
except Exception as e:
    print(f"   ERROR: {e}")

# Test 3: OPTIONS request (CORS preflight)
print("\n3. Testing CORS preflight (OPTIONS)...")
try:
    response = requests.options(
        "http://localhost:8000/api/tasks",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "authorization"
        }
    )
    print(f"   Status: {response.status_code}")
    print(f"   Access-Control-Allow-Origin: {response.headers.get('Access-Control-Allow-Origin', 'NOT SET')}")
    print(f"   Access-Control-Allow-Methods: {response.headers.get('Access-Control-Allow-Methods', 'NOT SET')}")
    print(f"   Access-Control-Allow-Headers: {response.headers.get('Access-Control-Allow-Headers', 'NOT SET')}")
except Exception as e:
    print(f"   ERROR: {e}")

print("\n" + "=" * 70)
print("If CORS headers are 'NOT SET', backend needs to be restarted!")
