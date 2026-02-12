import jwt
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from the backend directory
load_dotenv(dotenv_path='F:/hackthone_todo_vibecode/phase_02/backend/.env')

# Load the same secret key as used by the backend
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "fallback_dev_secret_for_testing_only")
ALGORITHM = "HS256"

print(f"Using SECRET_KEY: {SECRET_KEY}")

# A token from our test
token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiOGI5YTk4NjItOGQ1My00MDE0LTk3YjEtMzJhYWZlMmY4Y2VjIiwiZW1haWwiOiJmaW5hbHdvcmtpbmd0ZXN0QGV4YW1wbGUuY29tIiwiZXhwIjoxNzY4MjI1MTM4fQ.Og43EwYZX5yN5cep5j63EB-EEqp4VGLIRItjpjNZQ5g"

try:
    print("Attempting to decode token...")
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print(f"Decoded payload: {payload}")
    
    # Check if token is expired
    exp = payload.get("exp")
    current_time = datetime.utcnow().timestamp()
    print(f"Current time: {current_time}")
    print(f"Token exp: {exp}")
    print(f"Is expired: {current_time > exp}")
    
    if current_time <= exp:
        print("Token is valid and not expired!")
    else:
        print("Token is expired!")
        
except jwt.ExpiredSignatureError:
    print("Token has expired!")
except jwt.InvalidTokenError as e:
    print(f"Invalid token: {e}")
except Exception as e:
    print(f"Other error: {e}")