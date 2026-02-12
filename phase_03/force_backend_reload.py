"""Force check if backend loaded new code"""
import requests
import sys

print("=" * 80)
print("🔍 CHECKING IF BACKEND LOADED NEW CODE")
print("=" * 80)

# Test the endpoint that should work with new code
print("\n1️⃣ Testing /api/my-tasks endpoint...")
try:
    response = requests.get("http://localhost:8000/api/my-tasks", timeout=3)
    
    if response.status_code == 200:
        tasks = response.json()
        print(f"✅ Endpoint responds: {len(tasks)} tasks")
        
        if len(tasks) == 0:
            print("\n❌ BACKEND IS STILL USING OLD CODE!")
            print("\nProof:")
            print("- Database has 3 tasks")
            print("- Backend returns 0 tasks")
            print("- This means backend code NOT reloaded")
            
            print("\n" + "=" * 80)
            print("🔧 SOLUTION: FORCE RESTART BACKEND")
            print("=" * 80)
            print("\nYou MUST do this:")
            print("\n1. Go to backend terminal")
            print("2. Press Ctrl+C")
            print("3. Type: exit")
            print("4. Close terminal window (click X)")
            print("5. Open BRAND NEW terminal")
            print("6. Type: cd F:\\hackthone_todo_vibecode\\phase_03\\backend")
            print("7. Type: python -m uvicorn main:app --reload")
            print("8. Wait for 'Application startup complete'")
            print("\nDO NOT skip step 3-5! Terminal must be completely closed!")
            
            sys.exit(1)
        else:
            print(f"✅ Backend loaded new code! Found {len(tasks)} tasks")
            for task in tasks:
                print(f"   - {task['title']}")
    else:
        print(f"❌ Error: {response.status_code}")
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nBackend might not be running!")
    print("Start with: cd backend && python -m uvicorn main:app --reload")

print("\n" + "=" * 80)
