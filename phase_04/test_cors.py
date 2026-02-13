"""Test CORS configuration."""
import requests

# Test OPTIONS request (preflight)
print("Testing CORS preflight request...")
try:
    response = requests.options(
        "http://localhost:8000/api/tasks",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "authorization,content-type"
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    
    # Check for CORS headers
    if "access-control-allow-origin" in response.headers:
        print("✅ CORS headers present!")
    else:
        print("❌ CORS headers missing!")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*60 + "\n")

# Test actual GET request
print("Testing GET request with CORS...")
try:
    response = requests.get(
        "http://localhost:8000/api/tasks",
        headers={
            "Origin": "http://localhost:3000",
        }
    )
    print(f"Status: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    
    if "access-control-allow-origin" in response.headers:
        print("✅ CORS headers present!")
    else:
        print("❌ CORS headers missing!")
        
except Exception as e:
    print(f"❌ Error: {e}")
