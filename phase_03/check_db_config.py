import os
import sys

# Add the backend/src directory to the path so imports work correctly
sys.path.insert(0, os.path.join(os.getcwd(), 'backend', 'src'))

from config import settings

print("Database URL from settings:", settings.database_url)

# Check all environment variables that might be affecting this
print("\nRelevant environment variables:")
for var in ['DATABASE_URL', 'ENVIRONMENT', 'BETTER_AUTH_SECRET']:
    value = os.environ.get(var, 'NOT SET')
    print(f"{var}: {value[:50]}{'...' if len(str(value)) > 50 else ''}")