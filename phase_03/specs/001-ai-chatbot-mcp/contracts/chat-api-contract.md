# API Contract: AI Chatbot with MCP

## POST /api/{user_id}/chat

### Description
Accepts user natural language input and returns AI response with invoked MCP tools. Creates or resumes a conversation.

### Path Parameters
- **user_id** (string, required): The ID of the user initiating the chat

### Request Headers
- **Authorization** (string, required): Bearer token for JWT authentication
- **Content-Type** (string, required): application/json

### Request Body
```json
{
  "message": "string (required): The user's natural language input",
  "conversation_id": "string (optional): ID of existing conversation to continue"
}
```

### Response Codes
- **200**: Success - returns AI response and tool invocation results
- **400**: Bad Request - invalid request format
- **401**: Unauthorized - invalid or missing JWT
- **403**: Forbidden - JWT user_id doesn't match path user_id
- **404**: Not Found - conversation not found (if conversation_id provided)
- **500**: Internal Server Error - unexpected server error

### Successful Response (200)
```json
{
  "conversation_id": "string: ID of the conversation",
  "response": "string: AI-generated response to the user",
  "tool_calls": [
    {
      "tool_name": "string: Name of the MCP tool called",
      "arguments": "object: Arguments passed to the tool",
      "result": "object: Result from the tool execution"
    }
  ],
  "timestamp": "string: ISO 8601 timestamp of the response"
}
```

### Error Response (4xx/5xx)
```json
{
  "error": {
    "code": "string: Error code",
    "message": "string: Human-readable error message",
    "details": "object: Additional error details (optional)"
  }
}
```

## Security
- Requires valid JWT in Authorization header
- Validates that JWT's user_id matches the path parameter user_id
- Enforces user ownership on all accessed resources

## Rate Limiting
- TBD: Specific rate limits to be defined based on usage patterns