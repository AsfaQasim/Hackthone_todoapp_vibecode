"""Test backend login directly with detailed error"""
import requests
import json

BACKEND_URL = "http://localhost:8000"

print("=" * 80)
print("🧪 TESTING BACKEND LOGIN DIRECTLY")
print("=" * 80)

print("\n📝 Sending login request...")
try:
    response = requests.post(
        f"{BACKEND_URL}/login",
        json={"email": "test@example.com", "password": "test123"},
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code != 200:
        print(f"\n❌ Login failed!")
        print(f"\n💡 Check backend terminal for detailed error logs")
        print(f"   Look for:")
        print(f"   - Database connection errors")
        print(f"   - Table not found errors")
        print(f"   - Python exceptions")
    else:
        print(f"\n✅ Login successful!")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
