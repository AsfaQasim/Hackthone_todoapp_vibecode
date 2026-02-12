import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="../backend/.env")

# JWT configuration - using BETTER_AUTH_SECRET for Better Auth compatibility
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "fallback_dev_secret_for_testing_only")
print(f"SECRET_KEY: {SECRET_KEY}")
print(f"SECRET_KEY length: {len(SECRET_KEY)}")