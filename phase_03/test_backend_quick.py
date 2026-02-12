"""Quick backend test"""
import requests
import time

print("🧪 Quick Backend Test")
print("=" * 60)

try:
    # Test the endpoint
    print("\n1️⃣ Testing /api/my-tasks...")
    start = time.time()
    response = requests.get("http://localhost:8000/api/my-tasks", timeout=5)
    elapsed = time.time() - start
    
    print(f"Status: {response.status_code}")
    print(f"Time: {elapsed:.2f}s")
    
    if response.ok:
        tasks = response.json()
        print(f"✅ Got {len(tasks)} tasks")
        
        if tasks:
            for task in tasks[:3]:
                print(f"  - {task['title']}")
        else:
            print("⚠️ No tasks returned!")
            print("\n🔧 Backend needs restart!")
            print("Steps:")
            print("1. Go to backend terminal")
            print("2. Press Ctrl+C")
            print("3. Run: python -m uvicorn main:app --reload")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)
        
except requests.exceptions.Timeout:
    print("❌ Request timed out!")
    print("Backend might be stuck or not running")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
