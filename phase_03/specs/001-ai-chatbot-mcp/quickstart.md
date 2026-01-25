# Quickstart Guide: AI Chatbot with MCP

## Overview
This guide will help you quickly set up and run the AI Chatbot with MCP functionality.

## Prerequisites
- Python 3.11+
- Access to OpenAI API (for AI agent)
- Neon PostgreSQL database
- Existing Better Auth JWT tokens

## Setup

### 1. Clone and Navigate
```bash
git clone <repository-url>
cd backend
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file in the backend directory with the following variables:
```env
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL="postgresql://username:password@ep-host.aws.neon.tech/neondb?sslmode=require"
BETTER_AUTH_SECRET=your_better_auth_secret
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

### 4. Database Setup
Run the database migrations to create the required tables:
```bash
# Using your preferred migration tool
alembic upgrade head
```

### 5. Run the Server
```bash
uvicorn main:app --reload
```

## Usage

### 1. Obtain JWT Token
Get a valid JWT token from your Better Auth system.

### 2. Make a Chat Request
```bash
curl -X POST "http://127.0.0.1:8000/api/{user_id}/chat" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy groceries"
  }'
```

### 3. Expected Response
```json
{
  "conversation_id": "uuid-string",
  "response": "Task 'buy groceries' has been added successfully.",
  "tool_calls": [
    {
      "tool_name": "add_task",
      "arguments": {
        "title": "buy groceries"
      },
      "result": {
        "success": true,
        "task_id": "uuid-string"
      }
    }
  ],
  "timestamp": "2026-01-25T10:00:00Z"
}
```

## Key Components

### MCP Tools Available
- `add_task`: Create a new task
- `list_tasks`: Retrieve user's tasks
- `complete_task`: Mark a task as completed
- `delete_task`: Remove a task
- `update_task`: Modify an existing task

### Architecture Highlights
- Stateless server design
- All data persisted in Neon PostgreSQL
- AI agent communicates with backend only through MCP tools
- JWT authentication enforced on every request

## Troubleshooting

### Common Issues
1. **Authentication Errors**: Verify JWT token validity and ensure user_id in token matches the path parameter
2. **Database Connection**: Check that Neon PostgreSQL connection string is correct
3. **OpenAI API**: Confirm API key is valid and has sufficient quota

### Logs
Check server logs for detailed error information:
```bash
tail -f logs/app.log
```