"""Check if backend is running"""
import requests

print("=" * 80)
print("🔍 CHECKING IF BACKEND IS RUNNING")
print("=" * 80)

try:
    print("\n1️⃣ Testing backend health endpoint...")
    response = requests.get("http://localhost:8000/health", timeout=3)
    
    if response.ok:
        print("✅ Backend is RUNNING!")
        print(f"Response: {response.json()}")
    else:
        print(f"❌ Backend returned error: {response.status_code}")
        
except requests.exceptions.ConnectionError:
    print("❌ Backend is NOT RUNNING!")
    print("\n🔧 Start backend with:")
    print("   cd backend")
    print("   python -m uvicorn main:app --reload")
    
except requests.exceptions.Timeout:
    print("❌ Backend is not responding (timeout)")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 80)
