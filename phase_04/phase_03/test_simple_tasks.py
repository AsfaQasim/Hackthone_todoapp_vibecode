"""Simple test to check if tasks endpoint works."""

import requests

BASE_URL = "http://localhost:8000"

# Use a real token from the user
# You need to get this from the browser after logging in
TOKEN = input("Paste your auth token here: ").strip()

print("\n🧪 Testing /api/tasks endpoint...")
print("=" * 60)

# Test GET /api/tasks
print("\n1️⃣ Fetching tasks...")
response = requests.get(
    f"{BASE_URL}/api/tasks",
    headers={"Authorization": f"Bearer {TOKEN}"}
)

print(f"Status: {response.status_code}")
print(f"Response: {response.text[:500]}")

if response.status_code == 200:
    tasks = response.json()
    print(f"\n✅ Success! Found {len(tasks)} tasks")
    if tasks:
        print("\n📋 Tasks:")
        for task in tasks[:5]:
            print(f"   - {task.get('title')} ({task.get('status')})")
else:
    print(f"\n❌ Failed: {response.status_code}")

print("\n" + "=" * 60)
