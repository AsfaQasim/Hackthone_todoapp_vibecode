# Data Model: AI Chatbot with MCP

## Entities

### User
- **Fields**:
  - id: UUID (primary key)
  - email: String (unique)
  - name: String
  - created_at: DateTime
  - updated_at: DateTime

### Task
- **Fields**:
  - id: UUID (primary key)
  - title: String
  - description: Text (optional)
  - status: Enum ('pending', 'in_progress', 'completed')
  - user_id: UUID (foreign key to User)
  - created_at: DateTime
  - updated_at: DateTime
  - completed_at: DateTime (optional)

### Conversation
- **Fields**:
  - id: UUID (primary key)
  - user_id: UUID (foreign key to User)
  - title: String (derived from first message or AI)
  - created_at: DateTime
  - updated_at: DateTime

### Message
- **Fields**:
  - id: UUID (primary key)
  - conversation_id: UUID (foreign key to Conversation)
  - role: Enum ('user', 'assistant')
  - content: Text
  - timestamp: DateTime
  - metadata: JSON (optional, for tool calls and responses)

## Relationships
- User has many Tasks
- User has many Conversations
- Conversation has many Messages
- Message belongs to Conversation

## Validation Rules
- Task.title is required and must be between 1-255 characters
- Task.status must be one of the defined enum values
- User.email must be unique and valid email format
- Message.role must be either 'user' or 'assistant'
- All entities must have valid user_id for ownership validation

## State Transitions
- Task: pending → in_progress → completed (only forward transitions allowed)
- Task: completed tasks can be reopened to in_progress or pending