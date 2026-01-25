<!-- SYNC IMPACT REPORT
Version change: N/A -> 1.0.0
Modified principles: N/A (new constitution)
Added sections: All sections from Phase 3 Spec Constitution
Removed sections: None
Templates requiring updates: ✅ updated (.specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md), ✅ README.md updated
Follow-up TODOs: None
-->

# Phase 3 AI Chatbot with MCP Constitution

## Core Principles

### 1. Stateless Server Principle
The FastAPI server MUST NOT store any conversation or task state in memory. Every request to `/api/{user_id}/chat` is handled independently. All state MUST be persisted in the database. ❌ No global variables, ❌ No in-memory conversation cache, ❌ No session-based chat memory.
<!-- Ensuring correct use of AI agents and MCP architecture, preventing state leakage or improper coupling -->

### 2. Database as the Only Source of Truth
Tasks, conversations, and messages MUST be stored in Neon PostgreSQL. AI agents MUST NOT assume context unless retrieved from the database. After server restart, the system MUST resume conversations correctly.
<!-- Guaranteeing consistency across frontend, backend, agent, and tools -->

### 3. MCP-Only Task Operations Rule
AI agents MUST NEVER access the database directly. All task operations MUST be performed via MCP tools only. Allowed: Agent → MCP tool → Database. Forbidden: Agent → ORM / SQL / Repository.
<!-- Ensuring correct use of AI agents and MCP architecture, preventing improper coupling -->

### 4. Tool-Driven Intelligence
The agent's role is to reason and decide, not to execute logic. The agent MUST choose an MCP tool when user intent matches a task operation. Example: "Add a task" → add_task, "What's pending" → list_tasks.
<!-- Defining the role of AI agents in the system architecture -->

### 5. Deterministic Tool Selection
For the same user intent, the agent SHOULD select the same MCP tool. Ambiguous requests MUST trigger clarification instead of guessing.
<!-- Ensuring consistent agent behavior across interactions -->

### 6. Confirmation Requirement
Every successful tool action MUST be followed by a confirmation message. Example: "✅ Task 'Buy groceries' has been added successfully."
<!-- Ensuring clear feedback to users about system actions -->

### 7. Stateless MCP Tools
MCP tools MUST NOT store any internal state. Tools receive all required data via parameters. Tools persist results directly to the database.
<!-- Maintaining clean separation of concerns in the architecture -->

### 8. Ownership Enforcement
Every MCP tool MUST validate `user_id`. Tools MUST NOT modify or return tasks belonging to another user.
<!-- Ensuring security and proper user data isolation -->

### 9. Explicit Inputs & Outputs
Each MCP tool MUST define required parameters, optional parameters, and exact return schema. Implicit behavior is forbidden.
<!-- Ensuring predictable and well-defined interfaces between components -->

### 10. JWT Enforcement
All chat and MCP requests MUST require a valid JWT. Requests without valid JWT MUST return `401 Unauthorized`.
<!-- Ensuring secure access to system resources -->

### 11. User Identity Consistency
`user_id` extracted from JWT MUST MATCH the `user_id` in API path. Mismatch MUST result in `403 Forbidden`.
<!-- Ensuring proper authentication and authorization flow -->

### 12. Message Persistence
Every user message MUST be stored before agent execution. Every assistant response MUST be stored after agent execution.
<!-- Ensuring conversation continuity and audit trail -->

### 13. Role Integrity
Message roles are limited to `user` and `assistant`. System messages MUST NOT be stored in the database.
<!-- Maintaining clean message structure and data integrity -->

### 14. Graceful Failures
Task not found, invalid IDs, or ambiguous intent MUST NOT crash the agent. The agent MUST respond politely and informatively. Example: "⚠️ I couldn't find task 7. Please check the task number."
<!-- Ensuring robust error handling and user experience -->

### 15. No Silent Failures
Every failed MCP tool call MUST return a clear error response. The agent MUST translate errors into user-friendly messages.
<!-- Ensuring transparency in system behavior and error reporting -->

### 16. Dumb UI Rule
Frontend MUST NOT contain task logic. Frontend MUST ONLY send user messages, display responses, and render chat history.
<!-- Maintaining clear separation between UI and business logic -->

### 17. Token Handling
Frontend MUST attach JWT token to every chat request. Frontend MUST NOT decode or interpret token payload.
<!-- Ensuring proper authentication flow in the frontend -->

### 18. Extensibility Constraints
Adding new task operations MUST be done via new MCP tools. Agent behavior MUST be updated through specs, not hardcoded logic.
<!-- Ensuring maintainable and scalable architecture -->

## Additional Constraints

### Non-Negotiable Acceptance Criteria
Phase 3 is considered complete ONLY IF: ✅ All task actions are done via MCP tools, ✅ Server is fully stateless, ✅ Conversations persist across restarts, ✅ JWT auth is enforced everywhere, ✅ Agent behavior matches specs, ✅ No direct DB access from agent.
<!-- Defining clear completion criteria for the phase -->

## Development Workflow

### Final Authority Statement
This Spec Constitution is the highest authority document for Phase 3. Claude Code, human developers, and future phases MUST follow it strictly. Violations invalidate the Phase 3 implementation.
<!-- Establishing governance and compliance requirements -->

## Governance
This constitution serves as the ultimate source of truth for Phase 3 behavior. If any spec, code, or instruction conflicts with this constitution, this document wins. All implementation decisions by humans or Claude Code must comply with this document. All PRs/reviews must verify compliance with these principles.

**Version**: 1.0.0 | **Ratified**: 2026-01-25 | **Last Amended**: 2026-01-25