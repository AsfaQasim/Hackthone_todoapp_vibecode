"""Test the new /api/my-tasks endpoint"""
import requests

BACKEND_URL = "http://localhost:8000"

print("=" * 80)
print("🧪 TESTING /api/my-tasks ENDPOINT")
print("=" * 80)

print("\n📋 Fetching tasks from /api/my-tasks...")
try:
    response = requests.get(f"{BACKEND_URL}/api/my-tasks")
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        tasks = response.json()
        print(f"✅ Got {len(tasks)} tasks!")
        
        if len(tasks) > 0:
            print(f"\n📋 Tasks:")
            for i, task in enumerate(tasks[:10], 1):
                print(f"   {i}. {task.get('title')} ({task.get('status')})")
                print(f"      ID: {task.get('id')}")
                print(f"      User ID: {task.get('user_id')}")
        else:
            print(f"\n⚠️  No tasks found!")
            print(f"   This means:")
            print(f"   1. User 'asfaqasim145@gmail.com' not in database, OR")
            print(f"   2. User has no tasks")
    else:
        print(f"❌ Error: {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 80)
print("💡 If this works, we can use this endpoint in frontend!")
print("=" * 80)
