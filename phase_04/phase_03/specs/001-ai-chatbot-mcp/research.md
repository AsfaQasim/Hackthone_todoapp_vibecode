# Research: AI Chatbot with MCP

## Decision: AI Agent Framework
**Rationale**: Selected OpenAI's Assistants API for natural language understanding and intent detection due to its advanced capabilities in interpreting user requests and managing conversation context. The API provides reliable tool calling functionality that fits our MCP tool integration requirements.

**Alternatives considered**: 
- LangChain with various LLM providers
- Anthropic Claude with tool use
- Self-hosted models like Llama 2/3

## Decision: MCP SDK Implementation
**Rationale**: Implementing a custom MCP SDK that wraps our backend task operations ensures compliance with the constitutional requirement that agents never access the database directly. The SDK provides a clean interface for the AI agent to perform task operations.

**Alternatives considered**:
- Using existing MCP implementations
- Creating direct API call abstractions

## Decision: Conversation Storage Model
**Rationale**: Storing conversations and messages in the Neon PostgreSQL database ensures persistence across server restarts and maintains the stateless server architecture. Each conversation is associated with a user and contains ordered messages.

**Alternatives considered**:
- Using Redis for temporary storage
- File-based storage
- Separate document database

## Decision: Authentication Approach
**Rationale**: Leveraging the existing Better Auth JWT implementation ensures consistency with the Phase 2 system while meeting constitutional requirements for JWT enforcement and user identity consistency.

**Alternatives considered**:
- Custom JWT implementation
- OAuth2 tokens
- Session-based authentication (rejected due to statelessness requirement)

## Decision: Message Persistence Strategy
**Rationale**: Implementing a two-phase approach where user messages are stored before agent processing and assistant responses are stored after processing ensures complete conversation history is maintained while satisfying constitutional requirements.

**Alternatives considered**:
- Batch processing of message pairs
- Asynchronous message storage