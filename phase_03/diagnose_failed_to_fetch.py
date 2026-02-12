"""Diagnose Failed to Fetch error"""
import requests
import time

print("=" * 80)
print("🔍 DIAGNOSING 'FAILED TO FETCH' ERROR")
print("=" * 80)

# Test 1: Is backend running?
print("\n1️⃣ Is backend running on port 8000?")
try:
    response = requests.get("http://localhost:8000/health", timeout=2)
    if response.ok:
        print("   ✅ YES - Backend is running")
        print(f"   Response: {response.json()}")
    else:
        print(f"   ❌ Backend error: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("   ❌ NO - Backend is NOT running!")
    print("\n   🔧 START BACKEND:")
    print("      cd backend")
    print("      python -m uvicorn main:app --reload")
    print("\n   Then run this test again.")
    exit(1)
except Exception as e:
    print(f"   ❌ Error: {e}")
    exit(1)

# Test 2: Can we reach /api/my-tasks?
print("\n2️⃣ Can we reach /api/my-tasks endpoint?")
try:
    response = requests.get("http://localhost:8000/api/my-tasks", timeout=2)
    print(f"   Status: {response.status_code}")
    if response.ok:
        tasks = response.json()
        print(f"   ✅ Endpoint reachable - Returns {len(tasks)} tasks")
        
        if len(tasks) == 0:
            print("   ⚠️ Backend returns 0 tasks (old code still loaded)")
        else:
            print("   ✅ Backend has new code!")
            for task in tasks[:3]:
                print(f"      - {task['title']}")
    else:
        print(f"   ❌ Error: {response.status_code}")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 3: Is frontend running?
print("\n3️⃣ Is frontend running on port 3000?")
try:
    response = requests.get("http://localhost:3000", timeout=2)
    if response.ok or response.status_code == 404:
        print("   ✅ YES - Frontend is running")
    else:
        print(f"   ⚠️ Frontend status: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("   ❌ NO - Frontend is NOT running!")
    print("\n   🔧 START FRONTEND:")
    print("      cd frontend")
    print("      npm run dev")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Test 4: Check CORS
print("\n4️⃣ Is CORS configured correctly?")
try:
    response = requests.get(
        "http://localhost:8000/api/my-tasks",
        headers={'Origin': 'http://localhost:3000'},
        timeout=2
    )
    cors = response.headers.get('access-control-allow-origin', 'NOT SET')
    print(f"   CORS Header: {cors}")
    if cors in ['*', 'http://localhost:3000']:
        print("   ✅ CORS is OK")
    else:
        print("   ⚠️ CORS might be an issue")
except Exception as e:
    print(f"   ❌ Error: {e}")

# Summary
print("\n" + "=" * 80)
print("📊 DIAGNOSIS SUMMARY")
print("=" * 80)

print("\n💡 MOST LIKELY CAUSES OF 'FAILED TO FETCH':")
print("\n1. Backend not running")
print("   Solution: cd backend && python -m uvicorn main:app --reload")
print("\n2. Frontend not running")
print("   Solution: cd frontend && npm run dev")
print("\n3. Backend running but old code loaded")
print("   Solution: Kill Python and restart backend")
print("   Command: taskkill /F /IM python.exe")
print("   Then: cd backend && python -m uvicorn main:app --reload")
print("\n4. Browser cache issue")
print("   Solution: Clear cache (Ctrl+Shift+Delete) or use Incognito")

print("\n" + "=" * 80)
print("🔧 QUICK FIX:")
print("=" * 80)
print("\n1. Run: taskkill /F /IM python.exe")
print("2. Run: cd backend && python -m uvicorn main:app --reload")
print("3. Wait for 'Application startup complete'")
print("4. Refresh browser (or use Incognito mode)")
print("\n" + "=" * 80)
