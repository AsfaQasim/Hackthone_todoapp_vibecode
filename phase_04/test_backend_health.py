import requests

backend_url = "https://hackthone-todoapp-vibecode-nudz.vercel.app"

print(f"Testing backend at: {backend_url}")
print("=" * 60)

# Test health endpoint
try:
    response = requests.get(f"{backend_url}/health")
    print(f"✅ Health check: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ Health check failed: {e}")

print("=" * 60)

# Test root endpoint
try:
    response = requests.get(backend_url)
    print(f"✅ Root endpoint: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ Root endpoint failed: {e}")
