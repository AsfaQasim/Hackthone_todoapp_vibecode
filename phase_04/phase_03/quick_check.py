#!/usr/bin/env python3
import requests

print("Quick System Check")
print("=" * 50)

# Test 1: Backend
print("\n1. Backend Health...")
try:
    r = requests.get("http://localhost:8000/health", timeout=3)
    print(f"   ✅ Backend running: {r.status_code}")
except Exception as e:
    print(f"   ❌ Backend error: {e}")

# Test 2: Frontend
print("\n2. Frontend...")
try:
    r = requests.get("http://localhost:3000", timeout=3)
    print(f"   ✅ Frontend running: {r.status_code}")
except Exception as e:
    print(f"   ❌ Frontend error: {e}")

# Test 3: Login
print("\n3. Login Test...")
try:
    r = requests.post(
        "http://localhost:8000/login",
        json={"email": "test@test.com", "password": "test"},
        timeout=3
    )
    print(f"   Status: {r.status_code}")
    if r.status_code == 200:
        print(f"   ✅ Auth working")
    else:
        print(f"   Response: {r.text[:100]}")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 50)
