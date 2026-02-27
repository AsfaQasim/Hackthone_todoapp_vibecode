"""Test my-tasks endpoint"""
import requests

print("Testing /api/my-tasks endpoint...")
print("=" * 60)

try:
    response = requests.get("http://localhost:8000/api/my-tasks", timeout=5)
    print(f"Status: {response.status_code}")
    
    if response.ok:
        tasks = response.json()
        print(f"✅ Success! Found {len(tasks)} tasks")
        
        for task in tasks:
            print(f"\nTask: {task['title']}")
            print(f"  ID: {task['id']}")
            print(f"  Status: {task['status']}")
            print(f"  Created: {task['created_at']}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"❌ Exception: {e}")
