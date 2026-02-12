"""Check available routes on the backend."""

import requests
import json

try:
    response = requests.get('http://localhost:8000/openapi.json')
    data = response.json()
    
    # Handle the JSON wrapper middleware
    if 'data' in data and isinstance(data['data'], str):
        openapi_spec = json.loads(data['data'])
    elif 'paths' in data:
        openapi_spec = data
    else:
        print("Could not parse OpenAPI spec")
        print(data)
        exit(1)
    
    print("Available Routes:")
    print("=" * 60)
    
    for path, methods in openapi_spec['paths'].items():
        for method in methods.keys():
            if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                print(f"{method.upper():6} {path}")
    
    print("=" * 60)
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
