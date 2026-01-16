import jwt
import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables from the backend directory
load_dotenv(dotenv_path='F:/hackthone_todo_vibecode/phase_02/backend/.env')

# Load the same secret key as used by the backend
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "fallback_dev_secret_for_testing_only")
ALGORITHM = "HS256"

print(f"Using SECRET_KEY: {SECRET_KEY}")

# Create a new token with the same data as in the failing token
data = {
    "user_id": "8b9a9862-8d53-4014-97b1-32aafe2f8cec",
    "email": "finalworkingtest@example.com",
    "exp": int((datetime.utcnow() + timedelta(hours=1)).timestamp())
}

print(f"Creating token with data: {data}")

# Create the token
new_token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
print(f"New token: {new_token}")

# Now try to decode the new token
try:
    print("\nTrying to decode the new token...")
    decoded_payload = jwt.decode(new_token, SECRET_KEY, algorithms=[ALGORITHM])
    print(f"Successfully decoded new token: {decoded_payload}")
except Exception as e:
    print(f"Failed to decode new token: {e}")

# Also try to decode the original token
original_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOGI5YTk4NjItOGQ1My00MDE0LTk3YjEtMzJhYWZlMmY4Y2VjIiwiZW1haWwiOiJmaW5hbHdvcmtpbmd0ZXN0QGV4YW1wbGUuY29tIiwiZXhwIjoxNzY4MjI1MTM4fQ.Og43EwYZX5yN5cep5j63EB-EEqp4VGLIRItjpjNZQ5g"

try:
    print("\nTrying to decode the original token...")
    original_payload = jwt.decode(original_token, SECRET_KEY, algorithms=[ALGORITHM])
    print(f"Successfully decoded original token: {original_payload}")
except Exception as e:
    print(f"Failed to decode original token: {e}")
    print("This confirms that the original token was created with a different secret key.")