"""Quick system verification script - checks if backend and key endpoints are working."""

import requests
import sys

def check_backend_health():
    """Check if backend is running and healthy."""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running and healthy")
            return True
        else:
            print(f"⚠️ Backend responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Backend is not running (connection refused)")
        print("   Start it with: cd backend && python main.py")
        return False
    except Exception as e:
        print(f"❌ Error checking backend: {e}")
        return False

def check_frontend():
    """Check if frontend is running."""
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code in [200, 304]:
            print("✅ Frontend is running")
            return True
        else:
            print(f"⚠️ Frontend responded with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Frontend is not running (connection refused)")
        print("   Start it with: cd frontend && npm run dev")
        return False
    except Exception as e:
        print(f"❌ Error checking frontend: {e}")
        return False

def check_openai_key():
    """Check if OpenAI API key is configured."""
    try:
        with open('.env', 'r') as f:
            content = f.read()
            if 'OPENAI_API_KEY=' in content and 'sk-' in content:
                print("✅ OpenAI API key is configured")
                return True
            else:
                print("⚠️ OpenAI API key might not be configured properly")
                return False
    except FileNotFoundError:
        print("⚠️ .env file not found")
        return False
    except Exception as e:
        print(f"❌ Error checking OpenAI key: {e}")
        return False

def main():
    """Run all verification checks."""
    print("=" * 60)
    print("SYSTEM VERIFICATION")
    print("=" * 60)
    print()
    
    backend_ok = check_backend_health()
    print()
    
    frontend_ok = check_frontend()
    print()
    
    openai_ok = check_openai_key()
    print()
    
    print("=" * 60)
    if backend_ok and frontend_ok and openai_ok:
        print("✅ ALL SYSTEMS OPERATIONAL")
        print()
        print("You can now:")
        print("  1. Open http://localhost:3000 in your browser")
        print("  2. Login or signup")
        print("  3. Go to /chat to use AI Assistant")
        print("  4. Go to /general-task-execution to see AI-created tasks")
    else:
        print("⚠️ SOME ISSUES DETECTED")
        print()
        if not backend_ok:
            print("  - Start backend: cd backend && python main.py")
        if not frontend_ok:
            print("  - Start frontend: cd frontend && npm run dev")
        if not openai_ok:
            print("  - Check .env file for OPENAI_API_KEY")
    print("=" * 60)
    
    return 0 if (backend_ok and frontend_ok and openai_ok) else 1

if __name__ == "__main__":
    sys.exit(main())
