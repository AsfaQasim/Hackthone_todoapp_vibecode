import sys
sys.path.append('./backend')

from backend.utils.jwt_handler import create_access_token, verify_better_auth_token
from datetime import timedelta
import os

# Set the secret
os.environ['BETTER_AUTH_SECRET'] = 'fallback_dev_secret_for_testing_only'

test_data = {'user_id': 'test-user-123', 'email': 'test@example.com'}
token = create_access_token(data=test_data, expires_delta=timedelta(hours=1))
print('Created token:', token[:50], '...')

# Let's manually decode the token to see what's inside
from jose import jwt
SECRET_KEY = os.getenv("BETTER_AUTH_SECRET", "fallback_dev_secret_for_testing_only")
ALGORITHM = "HS256"

try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    print("Decoded payload:", payload)
    
    # Now try verification
    token_data = verify_better_auth_token(token)
    if token_data:
        print('Verification successful!')
        print('User ID:', token_data.user_id)
        print('Email:', token_data.email)
        print('Exp:', token_data.exp)
    else:
        print('Verification failed')
except Exception as e:
    print(f"Error during verification: {e}")