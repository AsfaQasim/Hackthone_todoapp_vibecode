"""Test login with new secret."""
import requests
import jwt

print("Testing login with new secret...")
print("=" * 70)

# Test login
print("\n1. Logging in...")
response = requests.post(
    "http://localhost:8000/login",
    json={"email": "asfaqasim145@gmail.com", "password": "test123"}
)

print(f"Status: {response.status_code}")
data = response.json()
print(f"Response: {data}")

if 'token' in data or 'access_token' in data:
    token = data.get('token') or data.get('access_token')
    print(f"\n✅ Token received: {token[:50]}...")
    
    # Decode token
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        print(f"\nToken Payload:")
        print(f"  sub: {payload.get('sub')}")
        print(f"  email: {payload.get('email')}")
        print(f"  exp: {payload.get('exp')}")
    except Exception as e:
        print(f"Error decoding: {e}")
    
    # Test tasks API with new token
    print("\n2. Testing tasks API with new token...")
    response = requests.get(
        "http://localhost:8000/api/tasks",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    
    if response.status_code == 200:
        print("\n✅ SUCCESS! New token works!")
    else:
        print("\n❌ FAILED! Token still doesn't work")
else:
    print("\n❌ No token in response")

print("\n" + "=" * 70)
