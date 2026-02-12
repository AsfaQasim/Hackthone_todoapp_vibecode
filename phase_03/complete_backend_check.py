"""Complete backend diagnostic check"""
import requests
import time
import sys

def print_section(title):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def check_backend_health():
    """Check if backend is running"""
    print_section("1️⃣ BACKEND HEALTH CHECK")
    
    try:
        response = requests.get("http://localhost:8000/health", timeout=3)
        if response.ok:
            print("✅ Backend is RUNNING")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ Backend returned error: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is NOT RUNNING!")
        print("\n🔧 Start backend:")
        print("   cd backend")
        print("   python -m uvicorn main:app --reload")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_cors():
    """Check CORS configuration"""
    print_section("2️⃣ CORS CHECK")
    
    try:
        response = requests.get(
            "http://localhost:8000/health",
            headers={
                'Origin': 'http://localhost:3000',
                'Referer': 'http://localhost:3000/'
            }
        )
        
        cors_origin = response.headers.get('access-control-allow-origin', 'NOT SET')
        cors_creds = response.headers.get('access-control-allow-credentials', 'NOT SET')
        
        print(f"Access-Control-Allow-Origin: {cors_origin}")
        print(f"Access-Control-Allow-Credentials: {cors_creds}")
        
        if cors_origin in ['*', 'http://localhost:3000']:
            print("✅ CORS is configured correctly")
            return True
        else:
            print("⚠️ CORS might have issues")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_my_tasks_endpoint():
    """Check /api/my-tasks endpoint"""
    print_section("3️⃣ /api/my-tasks ENDPOINT CHECK")
    
    try:
        response = requests.get("http://localhost:8000/api/my-tasks", timeout=5)
        
        print(f"Status: {response.status_code}")
        
        if response.ok:
            tasks = response.json()
            print(f"✅ Endpoint working")
            print(f"   Tasks returned: {len(tasks)}")
            
            if len(tasks) > 0:
                print("\n   Tasks:")
                for task in tasks[:3]:
                    print(f"   - {task['title']}")
                return True
            else:
                print("\n⚠️ Endpoint works but returns 0 tasks")
                print("   This means backend code needs restart")
                return False
        else:
            print(f"❌ Endpoint error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_database_connection():
    """Check database connection"""
    print_section("4️⃣ DATABASE CONNECTION CHECK")
    
    try:
        # Try to import and check database
        import sys
        import os
        sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))
        
        from dotenv import load_dotenv
        load_dotenv('backend/.env')
        
        db_url = os.getenv('DATABASE_URL', '')
        
        if not db_url:
            print("❌ DATABASE_URL not found in backend/.env")
            return False
        
        print(f"Database URL: {db_url[:50]}...")
        
        # Check if it's PostgreSQL or SQLite
        if 'postgresql' in db_url.lower():
            print("✅ Using PostgreSQL (Neon)")
        elif 'sqlite' in db_url.lower():
            print("✅ Using SQLite (Local)")
        else:
            print("⚠️ Unknown database type")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_login_endpoint():
    """Check login endpoint"""
    print_section("5️⃣ LOGIN ENDPOINT CHECK")
    
    try:
        response = requests.post(
            "http://localhost:8000/login",
            json={
                "email": "asfaqasim145@gmail.com",
                "password": "test123"
            },
            timeout=5
        )
        
        print(f"Status: {response.status_code}")
        
        if response.ok:
            data = response.json()
            print("✅ Login working")
            print(f"   User ID: {data.get('user_id', 'N/A')}")
            print(f"   Token: {data.get('token', 'N/A')[:20]}...")
            return True
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_chat_endpoint():
    """Check chat endpoint"""
    print_section("6️⃣ CHAT ENDPOINT CHECK")
    
    try:
        # First login to get token
        login_response = requests.post(
            "http://localhost:8000/login",
            json={
                "email": "asfaqasim145@gmail.com",
                "password": "test123"
            }
        )
        
        if not login_response.ok:
            print("❌ Cannot test chat - login failed")
            return False
        
        login_data = login_response.json()
        token = login_data.get('token')
        user_id = login_data.get('user_id')
        
        # Try chat endpoint
        chat_response = requests.post(
            f"http://localhost:8000/api/{user_id}/chat",
            headers={
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            },
            json={
                'message': 'test message'
            },
            timeout=10
        )
        
        print(f"Status: {chat_response.status_code}")
        
        if chat_response.ok:
            data = chat_response.json()
            response_text = data.get('response', '')
            print("✅ Chat endpoint working")
            print(f"   Response: {response_text[:100]}...")
            return True
        else:
            print(f"❌ Chat failed: {chat_response.status_code}")
            print(f"   Response: {chat_response.text[:200]}")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def check_backend_logs():
    """Check if backend is logging properly"""
    print_section("7️⃣ BACKEND CONFIGURATION CHECK")
    
    try:
        import os
        
        # Check backend .env file
        env_path = 'backend/.env'
        if os.path.exists(env_path):
            print("✅ backend/.env exists")
            
            with open(env_path, 'r') as f:
                content = f.read()
                
            if 'DATABASE_URL' in content:
                print("✅ DATABASE_URL configured")
            else:
                print("❌ DATABASE_URL missing")
            
            if 'OPENAI_API_KEY' in content:
                print("✅ OPENAI_API_KEY configured")
            else:
                print("⚠️ OPENAI_API_KEY missing")
            
            if 'JWT_SECRET' in content:
                print("✅ JWT_SECRET configured")
            else:
                print("❌ JWT_SECRET missing")
            
            return True
        else:
            print("❌ backend/.env not found")
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("\n" + "🔍" * 40)
    print("     COMPLETE BACKEND DIAGNOSTIC CHECK")
    print("🔍" * 40)
    
    results = {
        'Backend Health': check_backend_health(),
        'CORS': check_cors(),
        'My Tasks Endpoint': check_my_tasks_endpoint(),
        'Database Connection': check_database_connection(),
        'Login Endpoint': check_login_endpoint(),
        'Chat Endpoint': check_chat_endpoint(),
        'Backend Config': check_backend_logs()
    }
    
    # Summary
    print_section("📊 SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for check, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {check}")
    
    print(f"\nScore: {passed}/{total} checks passed")
    
    # Recommendations
    print_section("💡 RECOMMENDATIONS")
    
    if not results['Backend Health']:
        print("🔧 Backend is not running!")
        print("   Action: Start backend")
        print("   Command: cd backend && python -m uvicorn main:app --reload")
    
    elif results['Backend Health'] and not results['My Tasks Endpoint']:
        print("🔧 Backend is running but returning wrong data")
        print("   Action: Restart backend to load new code")
        print("   Steps:")
        print("   1. Go to backend terminal")
        print("   2. Press Ctrl+C")
        print("   3. Close terminal completely")
        print("   4. Open new terminal")
        print("   5. cd backend")
        print("   6. python -m uvicorn main:app --reload")
    
    elif all(results.values()):
        print("✅ All checks passed!")
        print("   Backend is working correctly")
        print("   If frontend still shows 'Failed to fetch':")
        print("   1. Check frontend is running (npm run dev)")
        print("   2. Check frontend .env.local has NEXT_PUBLIC_API_URL=http://localhost:8000")
        print("   3. Clear browser cache or use Incognito mode")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    main()
