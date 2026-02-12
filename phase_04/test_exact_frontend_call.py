"""Test the exact call that frontend makes"""
import requests

print("=" * 80)
print("🧪 TESTING EXACT FRONTEND API CALL")
print("=" * 80)

# This is exactly what the frontend does
API_URL = "http://localhost:8000"
endpoint = f"{API_URL}/api/my-tasks"

print(f"\n📡 Calling: {endpoint}")
print("Method: GET")
print("Headers: Content-Type: application/json")

try:
    response = requests.get(
        endpoint,
        headers={"Content-Type": "application/json"},
        timeout=5
    )
    
    print(f"\n📥 Response:")
    print(f"Status: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    
    if response.ok:
        tasks = response.json()
        print(f"\n✅ SUCCESS!")
        print(f"Tasks returned: {len(tasks)}")
        
        if tasks:
            print("\n📋 Tasks:")
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task['title']}")
                print(f"   ID: {task['id'][:8]}...")
                print(f"   Status: {task['status']}")
        else:
            print("\n⚠️ No tasks returned (empty array)")
            print("\nPossible reasons:")
            print("1. Backend code not restarted")
            print("2. Database connection issue")
            print("3. User not found in database")
    else:
        print(f"\n❌ ERROR!")
        print(f"Response: {response.text}")
        
except requests.exceptions.ConnectionError as e:
    print(f"\n❌ CONNECTION ERROR!")
    print(f"Cannot connect to {endpoint}")
    print("\nBackend might not be running on port 8000")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")

print("\n" + "=" * 80)
