"""
Debug script to identify the exact cause of authentication failures
"""

import sys
import os
import logging

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Configure logging to see what's happening
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_routes():
    """Check all the route imports and dependencies"""
    print("Checking route imports and dependencies...")
    
    try:
        # Import main app to see if there are any import errors
        from backend.main import app
        print("[OK] Main app imports successfully")
    except Exception as e:
        print(f"[ERROR] Main app import failed: {e}")
        return False

    try:
        # Check the chat route specifically
        from backend.src.api.routes.chat import router as chat_router
        print("[OK] Chat router imports successfully")
    except Exception as e:
        print(f"[ERROR] Chat router import failed: {e}")
        return False

    try:
        # Check the auth middleware
        from backend.src.api.middleware.auth_middleware import auth_middleware
        print("[OK] Auth middleware imports successfully")
    except Exception as e:
        print(f"[ERROR] Auth middleware import failed: {e}")
        return False

    try:
        # Check the old auth middleware
        from backend.middleware.auth_middleware import JWTBearer, verify_user_is_authenticated
        print("[OK] Old auth middleware imports successfully")
    except Exception as e:
        print(f"[ERROR] Old auth middleware import failed: {e}")
        return False
    
    return True

def check_dependencies():
    """Check for conflicting dependencies"""
    print("\nChecking for dependency conflicts...")
    
    # Check if there are multiple auth dependencies being used
    import inspect
    
    try:
        from backend.src.api.routes.chat import chat
        # Get the function signature to see what dependencies it has
        sig = inspect.signature(chat)
        params = list(sig.parameters.keys())
        print(f"Chat endpoint parameters: {params}")
        
        # Check the get_authenticated_user function
        from backend.src.api.routes.chat import get_authenticated_user
        sig2 = inspect.signature(get_authenticated_user)
        params2 = list(sig2.parameters.keys())
        print(f"get_authenticated_user parameters: {params2}")
        
    except Exception as e:
        print(f"Error checking dependencies: {e}")
        return False
    
    return True

def check_middleware_conflicts():
    """Check if there are middleware conflicts"""
    print("\nChecking for middleware conflicts...")
    
    # The issue might be that both global middleware and route-level auth are active
    # Let's check how they interact
    
    print("Potential issue: Both global middleware and route-level auth might be conflicting")
    print("- Global middleware sets request.state.user and request.state.current_user")
    print("- Route-level auth (JWTBearer) might try to re-authenticate")
    print("- This could cause conflicts if not handled properly")
    
    return True

if __name__ == "__main__":
    print("Starting authentication debug process...\n")
    
    success = True
    success &= check_routes()
    success &= check_dependencies()
    success &= check_middleware_conflicts()
    
    if success:
        print("\n[OK] All checks passed - no obvious import or dependency issues found")
        print("\nPossible remaining issues:")
        print("1. Token format/expiration issues")
        print("2. User ID format mismatches")
        print("3. Frontend not sending proper Authorization header")
        print("4. Middleware conflicts not caught by imports")
        print("5. Database user lookup failures")
    else:
        print("\n[ERROR] Some checks failed - there are import or dependency issues")