"""Check frontend connection to backend"""
import requests
import json

print("=" * 80)
print("🔍 CHECKING FRONTEND CONNECTION")
print("=" * 80)

# Check what URL frontend is using
print("\n1️⃣ Checking frontend .env.local...")
try:
    with open('frontend/.env.local', 'r') as f:
        content = f.read()
        if 'NEXT_PUBLIC_API_URL' in content:
            lines = [line for line in content.split('\n') if 'NEXT_PUBLIC_API_URL' in line and not line.strip().startswith('#')]
            print(f"   Found {len(lines)} NEXT_PUBLIC_API_URL entries:")
            for line in lines:
                print(f"   {line}")
        else:
            print(f"   ❌ NEXT_PUBLIC_API_URL not found!")
except Exception as e:
    print(f"   ❌ Error reading .env.local: {e}")

# Check if frontend is running
print("\n2️⃣ Checking if frontend is running...")
try:
    response = requests.get("http://localhost:3000", timeout=5)
    if response.status_code == 200:
        print(f"   ✅ Frontend is running!")
    else:
        print(f"   ⚠️  Frontend returned: {response.status_code}")
except requests.exceptions.ConnectionError:
    print(f"   ❌ Frontend is NOT running!")
    print(f"   Please start frontend:")
    print(f"   cd frontend")
    print(f"   npm run dev")
except Exception as e:
    print(f"   ❌ Error: {e}")

print("\n" + "=" * 80)
print("📝 SOLUTION:")
print("=" * 80)
print("\n1. Make sure frontend .env.local has:")
print("   NEXT_PUBLIC_API_URL=http://localhost:8000")
print("\n2. Restart frontend:")
print("   - Go to frontend terminal")
print("   - Press Ctrl+C")
print("   - Run: npm run dev")
print("\n3. Clear browser cache:")
print("   - Press Ctrl+Shift+Delete")
print("   - Clear cache")
print("   - Reload page")
print("=" * 80)
