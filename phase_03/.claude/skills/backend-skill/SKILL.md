---
name: backend-skill
description: Build and manage backend APIs by generating routes, handling requests and responses, and connecting to databases.
---

# Backend Skill – API & Data Handling

## Instructions

1. **Route Generation**
   - Define RESTful API endpoints
   - Organize routes by feature or resource
   - Use clear and consistent naming conventions

2. **Request Handling**
   - Parse request bodies, query parameters, and headers
   - Validate incoming data before processing
   - Handle authentication and authorization when required

3. **Response Handling**
   - Return structured and consistent API responses
   - Use appropriate HTTP status codes
   - Handle errors and edge cases gracefully

4. **Database Connection**
   - Connect to databases securely
   - Execute queries safely and efficiently
   - Handle transactions and rollbacks when needed

## Best Practices
- Keep routes thin and move logic to services
- Validate all inputs and outputs
- Never expose internal errors or stack traces
- Use environment variables for secrets
- Follow REST API best practices
- Keep database access centralized

## Example Structure
```python
from fastapi import FastAPI, Depends

app = FastAPI()

@app.get("/users")
def get_users():
    return {"users": []}
