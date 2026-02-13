"""Check what secret the backend is using."""
import os
import sys

# Add backend to path
sys.path.insert(0, 'backend')
sys.path.insert(0, 'backend/src')

# Load environment
from dotenv import load_dotenv
load_dotenv('backend/.env')

print("Checking backend JWT secret...")
print("=" * 70)

# Check environment variables
better_auth = os.getenv("BETTER_AUTH_SECRET", "NOT SET")
jwt_secret = os.getenv("JWT_SECRET", "NOT SET")

print(f"\nFrom environment:")
print(f"  BETTER_AUTH_SECRET: {better_auth[:50]}...")
print(f"  JWT_SECRET: {jwt_secret[:50]}...")

# Check what auth_service is using
try:
    from src.services.auth_service import SECRET_KEY
    print(f"\nauth_service.py SECRET_KEY: {SECRET_KEY[:50]}...")
except Exception as e:
    print(f"\nError loading auth_service: {e}")

# Check config
try:
    from src.config import settings
    print(f"\nsettings.secret_key: {settings.secret_key[:50]}...")
    print(f"settings.jwt_secret: {settings.jwt_secret[:50]}...")
except Exception as e:
    print(f"\nError loading settings: {e}")

print("\n" + "=" * 70)
print("\nExpected secret (from frontend .env.local):")
print("NTdXaB5jI14he9VSyTL8uOoz5QOjOPwA4EM_RhZ3rFPIeLOPkLEE1fZaxFONGO4vDDfHPSdL2Q8dYGuhv6cq8g")
