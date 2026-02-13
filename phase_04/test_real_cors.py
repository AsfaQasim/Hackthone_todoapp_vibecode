"""Test CORS with actual browser-like headers."""
import requests

print("Testing CORS with browser-like request...")
print("=" * 70)

# Simulate a browser CORS preflight request
headers = {
    "Origin": "http://localhost:3000",
    "Access-Control-Request-Method": "GET",
    "Access-Control-Request-Headers": "authorization,content-type"
}

print("\nSending OPTIONS request (CORS preflight)...")
print(f"Headers: {headers}")

response = requests.options("http://localhost:8000/api/tasks", headers=headers)

print(f"\nResponse Status: {response.status_code}")
print("\nAll Response Headers:")
for key, value in response.headers.items():
    print(f"  {key}: {value}")

print("\n" + "=" * 70)

# Now test actual GET request
print("\nSending GET request with Origin header...")
response = requests.get(
    "http://localhost:8000/api/tasks",
    headers={"Origin": "http://localhost:3000"}
)

print(f"\nResponse Status: {response.status_code}")
print("\nAll Response Headers:")
for key, value in response.headers.items():
    print(f"  {key}: {value}")

print("\n" + "=" * 70)
if "access-control-allow-origin" in [k.lower() for k in response.headers.keys()]:
    print("✅ CORS headers are present!")
else:
    print("❌ CORS headers are MISSING!")
