"""Direct test of login endpoint to see actual error"""
import requests
import json

print("Testing login endpoint directly...")
print("=" * 60)

url = "http://localhost:8000/login"
data = {
    "email": "test@test.com",
    "password": "test123"
}

print(f"URL: {url}")
print(f"Data: {json.dumps(data, indent=2)}")
print("=" * 60)

try:
    response = requests.post(url, json=data)
    print(f"\n✅ Response Status: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    print(f"\nResponse Body:")
    print(json.dumps(response.json(), indent=2))
except Exception as e:
    print(f"\n❌ Error: {e}")
    print(f"Response text: {response.text if 'response' in locals() else 'No response'}")
