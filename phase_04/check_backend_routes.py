"""Check what routes are registered in the backend."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from main import app

print("=" * 80)
print("🔍 REGISTERED ROUTES IN BACKEND")
print("=" * 80)

task_routes = []
for route in app.routes:
    if hasattr(route, 'path') and hasattr(route, 'methods'):
        if 'task' in route.path.lower():
            task_routes.append({
                'path': route.path,
                'methods': list(route.methods),
                'name': route.name if hasattr(route, 'name') else 'N/A'
            })

print("\nTask-related routes:")
for route in task_routes:
    methods = ', '.join(route['methods'])
    print(f"  {methods:20} {route['path']}")

print("\n" + "=" * 80)
