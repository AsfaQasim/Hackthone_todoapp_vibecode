"""
Test script to verify environment variables and database connection
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Print the DATABASE_URL to verify it's loaded correctly
database_url = os.getenv("DATABASE_URL")
print(f"DATABASE_URL from environment: {database_url}")

if database_url and "localhost" in database_url:
    print("❌ ERROR: DATABASE_URL is pointing to localhost instead of Neon!")
    print("Please update your .env file with the correct Neon database URL")
elif database_url:
    print("✅ DATABASE_URL appears to be set correctly for Neon")
else:
    print("❌ ERROR: DATABASE_URL is not set in environment!")

print(f"BETTER_AUTH_SECRET is set: {'Yes' if os.getenv('BETTER_AUTH_SECRET') else 'No'}")
print(f"NEXT_PUBLIC_API_URL: {os.getenv('NEXT_PUBLIC_API_URL', 'Not set')}")