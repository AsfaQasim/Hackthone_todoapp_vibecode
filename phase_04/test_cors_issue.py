"""Test for CORS issues"""
import requests

print("=" * 80)
print("🧪 TESTING CORS AND BROWSER-LIKE REQUEST")
print("=" * 80)

# Simulate browser request with Origin header
headers = {
    'Content-Type': 'application/json',
    'Origin': 'http://localhost:3000',  # Frontend origin
    'Referer': 'http://localhost:3000/general-task-execution'
}

print(f"\n📡 Calling: http://localhost:8000/api/my-tasks")
print(f"Headers: {headers}")

try:
    response = requests.get(
        "http://localhost:8000/api/my-tasks",
        headers=headers,
        timeout=5
    )
    
    print(f"\n📥 Response:")
    print(f"Status: {response.status_code}")
    print(f"CORS Headers:")
    print(f"  Access-Control-Allow-Origin: {response.headers.get('access-control-allow-origin', 'NOT SET')}")
    print(f"  Access-Control-Allow-Credentials: {response.headers.get('access-control-allow-credentials', 'NOT SET')}")
    
    if response.ok:
        tasks = response.json()
        print(f"\n✅ Request successful!")
        print(f"Tasks: {len(tasks)}")
        
        if len(tasks) == 0:
            print("\n⚠️ Backend returned empty array")
            print("This means backend code needs restart!")
    else:
        print(f"\n❌ Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "=" * 80)
