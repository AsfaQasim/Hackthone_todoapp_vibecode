"""Simple test to verify the backend starts properly with new error handling."""

import subprocess
import time
import requests
import signal
import sys
import os

def test_backend_startup():
    """Test that the backend starts properly with new error handling."""
    print("Starting backend server...")
    
    # Start the backend server
    proc = subprocess.Popen([
        sys.executable, "-m", "uvicorn", 
        "backend.main:app", 
        "--host", "127.0.0.1", 
        "--port", "8000",
        "--reload"
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Give the server some time to start
    time.sleep(5)
    
    try:
        # Test the health endpoint
        response = requests.get("http://127.0.0.1:8000/health")
        print(f"Health check response: {response.status_code}")
        print(f"Health check data: {response.json()}")
        
        # Test that response is JSON
        assert response.headers.get('content-type', '').startswith('application/json'), \
            f"Response is not JSON: {response.headers.get('content-type')}"
        
        print("✓ Backend started successfully with proper JSON responses")
        
    except Exception as e:
        print(f"✗ Error testing backend: {e}")
        return False
    finally:
        # Terminate the server process
        proc.terminate()
        proc.wait()
        print("Backend server terminated.")
    
    return True

if __name__ == "__main__":
    success = test_backend_startup()
    if success:
        print("\n✓ All tests passed!")
    else:
        print("\n✗ Tests failed!")
        sys.exit(1)