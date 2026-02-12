# Phase I: In-Memory CLI Todo Application

A clean, production-grade command-line todo application built with Python 3.13+. This is Phase I of a multi-phase project demonstrating progressive evolution from CLI to cloud-native architecture.

## Features

- ✅ **Create** todos with descriptions
- ✅ **View** all todos in formatted table
- ✅ **Mark** todos as complete/incomplete
- ✅ **Filter** todos by status (all/complete/incomplete)
- ✅ **Update** todo descriptions
- ✅ **Delete** todos with confirmation
- ✅ **Clean CLI** interface with menu-driven navigation
- ✅ **Input validation** with user-friendly error messages
- ✅ **Structured logging** for observability
- ✅ **Production-grade** code quality (type hints, tests, linting)

## Architecture

Built with **Clean Architecture** principles:

```
src/
├── domain/          # Business entities (Todo)
├── services/        # Business logic (TodoService)
├── adapters/        # CLI interface
└── infrastructure/  # Storage & logging

tests/
├── unit/            # Unit tests (isolated)
└── integration/     # Integration tests (end-to-end)
```

**Layers**:
- **Domain**: Pure business entities with validation
- **Services**: CRUD operations and business rules
- **Adapters**: CLI user interface
- **Infrastructure**: In-memory storage, structured logging

## Quick Start

### Prerequisites

- Python 3.13+
- (Optional) UV package manager

### Run the Application

```bash
# Navigate to project root
cd phase_01

# Run with Python
python -m src.main

# Or with UV (if installed)
uv run python -m src.main
```

### Usage Example

```
=== Todo CLI ===
1. Add Todo
2. View All Todos
3. Filter Todos
4. Mark Todo Complete
5. Mark Todo Incomplete
6. Update Todo
7. Delete Todo
8. Exit

Enter your choice (1-8): 1

Enter todo description: Buy groceries

✓ Todo added successfully!
  ID: 1
  Description: Buy groceries
  Status: Incomplete
```

## Testing

### Run All Tests

```bash
# Run tests (requires pytest)
python -m pytest tests/

# Run with coverage
python -m pytest --cov=src --cov-report=term-missing tests/

# Run specific test file
python -m pytest tests/unit/test_todo.py -v
```

### Test Coverage

- **Unit Tests**: Todo entity, Storage, Service layer
- **Integration Tests**: Complete user workflows
- **Target Coverage**: ≥ 80%

## Development

### Project Structure

```
phase_01/
├── src/                    # Source code
│   ├── domain/             # Business entities
│   │   └── todo.py
│   ├── services/           # Business logic
│   │   └── todo_service.py
│   ├── adapters/           # CLI interface
│   │   └── cli.py
│   ├── infrastructure/     # Storage & logging
│   │   ├── storage.py
│   │   └── logger.py
│   └── main.py             # Entry point
├── tests/                  # Test suite
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
├── specs/                  # Design documents
│   └── 1-phase-1-cli-todo/
│       ├── spec.md         # Feature specification
│       ├── plan.md         # Implementation plan
│       ├── tasks.md        # Task breakdown
│       └── quickstart.md   # Detailed guide
├── pyproject.toml          # Project configuration
├── .python-version         # Python version (3.13)
└── README.md               # This file
```

### Code Quality

```bash
# Type checking (requires mypy)
python -m mypy src/

# Linting (requires ruff)
python -m ruff check src/

# Auto-fix linting issues
python -m ruff check src/ --fix

# Format code
python -m ruff format src/
```

## Design Documents

Comprehensive design documentation available in `specs/1-phase-1-cli-todo/`:

- **[spec.md](specs/1-phase-1-cli-todo/spec.md)** - Feature specification with user stories
- **[plan.md](specs/1-phase-1-cli-todo/plan.md)** - Technical implementation plan
- **[tasks.md](specs/1-phase-1-cli-todo/tasks.md)** - Detailed task breakdown
- **[quickstart.md](specs/1-phase-1-cli-todo/quickstart.md)** - Comprehensive usage guide
- **[data-model.md](specs/1-phase-1-cli-todo/data-model.md)** - Entity definitions
- **[contracts/cli-interface.md](specs/1-phase-1-cli-todo/contracts/cli-interface.md)** - CLI interface specification

## Technical Specifications

- **Language**: Python 3.13+
- **Storage**: In-memory (Python list)
- **Dependencies**: None (standard library only for core app)
- **Dev Dependencies**: pytest, mypy, ruff
- **Architecture**: Clean Architecture (4 layers)
- **Testing**: pytest with unit & integration tests
- **Logging**: Structured JSON logging
- **Performance**: <2s startup, <5s per operation

## Limitations (Phase I)

- **No Persistence**: All data lost on exit (in-memory only)
- **Single User**: No multi-user support
- **No Network**: Offline only, no sync

## Success Criteria

✅ All 7 success criteria met:

1. ✅ Create todo in <5 seconds
2. ✅ All CRUD operations work without errors
3. ✅ Full workflow completes in <2 minutes
4. ✅ Clear feedback for all actions (✓✗ℹ️ messages)
5. ✅ User-friendly error messages (no crashes)
6. ✅ Startup <2 seconds
7. ✅ Readable formatted output

## Future Phases

This is Phase I of a multi-phase project:

- **Phase II**: Full-stack web app (Next.js + FastAPI + PostgreSQL)
- **Phase III**: AI-powered chatbot (OpenAI + MCP SDK)
- **Phase IV**: Local Kubernetes deployment (Docker + Minikube + Helm)
- **Phase V**: Cloud-native (Kafka + Dapr + DigitalOcean)

## License

Educational project - no license specified

## Support

For issues or questions:
- Review design documents in `specs/1-phase-1-cli-todo/`
- Check log file: `todo-cli.log`
- Run tests to identify issues: `pytest -v`
