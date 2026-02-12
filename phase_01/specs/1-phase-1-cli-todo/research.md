# Research: Phase I In-Memory CLI Todo App

**Date**: 2026-01-02
**Feature**: Phase I In-Memory CLI Todo App
**Purpose**: Resolve technical unknowns and establish implementation approach

## 1. Python 3.13+ Project Setup with UV

### Decision: UV Project Structure

**Selected Approach**: Use UV with pyproject.toml for modern Python project management

**Setup Commands**:
```bash
# Initialize project
uv init --name todo-cli --python 3.13

# Add dev dependencies
uv add --dev pytest mypy ruff

# Run the application
uv run python -m src.main

# Run tests
uv run pytest

# Type check
uv run mypy src/

# Lint
uv run ruff check src/
```

**pyproject.toml Structure**:
```toml
[project]
name = "todo-cli"
version = "0.1.0"
description = "Phase I In-Memory CLI Todo Application"
requires-python = ">=3.13"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "mypy>=1.8.0",
    "ruff>=0.1.0",
]

[tool.ruff]
line-length = 100
target-version = "py313"

[tool.mypy]
python_version = "3.13"
strict = true
warn_return_any = true
warn_unused_configs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
```

**Rationale**:
- UV is modern, fast, and handles virtual environments automatically
- No external dependencies for core app (only dev dependencies)
- pyproject.toml is the standard for Python packaging
- Type checking and linting configured from the start

**Alternatives Considered**:
- pip + venv: Rejected (manual venv management, slower)
- poetry: Rejected (heavier, unnecessary for simple project)
- conda: Rejected (overkill for pure Python project)

---

## 2. CLI Best Practices in Python

### Decision: Menu-Driven Interface with Standard Library

**Selected Approach**: Use Python's built-in `input()` for menu-driven CLI

**Implementation Pattern**:
```python
def display_menu() -> None:
    """Display main menu options."""
    print("\n=== Todo CLI ===")
    print("1. Add Todo")
    print("2. View Todos")
    print("3. Mark Complete")
    print("4. Mark Incomplete")
    print("5. Filter Todos")
    print("6. Update Todo")
    print("7. Delete Todo")
    print("8. Exit")

def get_user_choice() -> str:
    """Get and validate user menu choice."""
    choice = input("\nEnter your choice (1-8): ").strip()
    return choice

def get_validated_input(prompt: str, validator: callable) -> str:
    """Get user input with validation."""
    while True:
        value = input(prompt).strip()
        try:
            validator(value)
            return value
        except ValueError as e:
            print(f"Error: {e}")
```

**Error Handling Pattern**:
- Use custom exceptions for domain errors (e.g., `TodoNotFoundError`)
- Catch exceptions at CLI boundary
- Display user-friendly messages
- Never expose stack traces to users

**User-Friendly Error Messages**:
```python
# Good: Clear, actionable
"Todo with ID 5 not found. Use 'View Todos' to see valid IDs."

# Bad: Technical
"KeyError: 5"
```

**Rationale**:
- Standard library only (no external CLI frameworks needed)
- Simple and clear for Python learners
- Easy to test (mock input/output)
- Menu-driven interface is discoverable (users see all options)

**Alternatives Considered**:
- argparse (command-line args): Rejected (less discoverable for learners)
- click/typer (CLI frameworks): Rejected (external dependencies, overkill)
- prompt_toolkit (advanced CLI): Rejected (too complex for Phase I)

---

## 3. Clean Architecture in Python

### Decision: Four-Layer Architecture

**Selected Approach**: Domain → Services → Adapters → Infrastructure

**Layer Responsibilities**:

1. **Domain Layer** (`src/domain/`):
   - Pure business entities (Todo class)
   - Validation rules
   - No dependencies on other layers
   - Example:
     ```python
     from dataclasses import dataclass
     from typing import Optional

     @dataclass
     class Todo:
         id: int
         description: str
         completed: bool = False

         def __post_init__(self) -> None:
             if not self.description or not self.description.strip():
                 raise ValueError("Description cannot be empty")
             if len(self.description) > 500:
                 raise ValueError("Description cannot exceed 500 characters")
     ```

2. **Service Layer** (`src/services/`):
   - Business logic (CRUD operations)
   - Depends on domain only
   - Injected with storage (infrastructure)
   - Example:
     ```python
     class TodoService:
         def __init__(self, storage: TodoStorage):
             self._storage = storage

         def create_todo(self, description: str) -> Todo:
             # Business logic here
             pass
     ```

3. **Adapter Layer** (`src/adapters/`):
   - External interfaces (CLI)
   - Depends on services and domain
   - Handles user I/O, formatting
   - Example:
     ```python
     class CLIAdapter:
         def __init__(self, service: TodoService):
             self._service = service

         def run(self) -> None:
             # CLI loop here
             pass
     ```

4. **Infrastructure Layer** (`src/infrastructure/`):
   - Cross-cutting concerns (storage, logging)
   - Implements interfaces defined by services
   - Example:
     ```python
     class InMemoryStorage:
         def __init__(self):
             self._todos: list[Todo] = []
             self._next_id: int = 1
     ```

**Dependency Injection Pattern**:
```python
# src/main.py
def main() -> None:
    # Setup infrastructure
    logger = setup_logger()
    storage = InMemoryStorage()

    # Setup service layer
    service = TodoService(storage, logger)

    # Setup adapter layer
    cli = CLIAdapter(service)

    # Run application
    cli.run()
```

**Rationale**:
- Clean separation enables testing each layer in isolation
- Domain layer is framework-agnostic (reusable in Phase II)
- Service layer contains all business logic (testable without CLI)
- Easy to add REST API adapter in Phase II without touching domain/services

**Alternatives Considered**:
- Flat structure (everything in one file): Rejected (not scalable, poor separation)
- MVC pattern: Rejected (doesn't fit CLI app, less clear for this domain)
- Hexagonal architecture: Rejected (same as clean architecture, just different naming)

---

## 4. Type Safety and Linting

### Decision: mypy for Type Checking, ruff for Linting

**Type Checking: mypy**

**Configuration**:
```toml
[tool.mypy]
python_version = "3.13"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_any_unimported = true
```

**Type Hint Best Practices**:
```python
from typing import Optional, Protocol

# Use built-in types for Python 3.13+
def get_todos(self) -> list[Todo]:  # Not List[Todo]
    pass

# Use Optional for nullable values
def find_by_id(self, id: int) -> Optional[Todo]:
    pass

# Use Protocol for structural typing (interfaces)
class TodoStorage(Protocol):
    def save(self, todo: Todo) -> None: ...
    def find_by_id(self, id: int) -> Optional[Todo]: ...
```

**Linting: ruff**

**Configuration**:
```toml
[tool.ruff]
line-length = 100
target-version = "py313"
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "UP",  # pyupgrade
]
```

**Rationale**:
- mypy is industry standard, excellent documentation
- ruff is fastest Python linter (100x faster than pylint)
- Both have good Python 3.13+ support
- Configuration is simple and maintainable

**Alternatives Considered**:
- pyright: Rejected (less common, harder to debug for learners)
- pylint: Rejected (much slower, more complex configuration)
- flake8: Rejected (ruff replaces it with better performance)

---

## 5. In-Memory Storage Patterns

### Decision: List-Based Storage with Sequential IDs

**Selected Approach**: Python list with sequential integer IDs

**Implementation Pattern**:
```python
class InMemoryStorage:
    def __init__(self) -> None:
        self._todos: list[Todo] = []
        self._next_id: int = 1

    def save(self, todo: Todo) -> Todo:
        """Save a new todo and assign ID."""
        todo.id = self._next_id
        self._next_id += 1
        self._todos.append(todo)
        return todo

    def find_by_id(self, id: int) -> Optional[Todo]:
        """Find todo by ID."""
        for todo in self._todos:
            if todo.id == id:
                return todo
        return None

    def find_all(self) -> list[Todo]:
        """Return all todos."""
        return self._todos.copy()  # Return copy to prevent external mutation

    def update(self, todo: Todo) -> None:
        """Update existing todo."""
        for i, existing in enumerate(self._todos):
            if existing.id == todo.id:
                self._todos[i] = todo
                return
        raise ValueError(f"Todo with ID {todo.id} not found")

    def delete(self, id: int) -> None:
        """Delete todo by ID."""
        self._todos = [t for t in self._todos if t.id != id]
```

**ID Generation Strategy**:
- Start at 1 (user-friendly)
- Increment sequentially
- Never reuse IDs (even after deletion)

**Data Structure Choice**:
- **List**: Simple, preserves order, good for small datasets (<1000 items)
- **Dict**: Could use `{id: todo}` for O(1) lookup, but list is sufficient for Phase I

**Thread Safety**:
- Not required for Phase I (single-threaded CLI)
- Can add threading.Lock in Phase II if needed

**Rationale**:
- List is simple and intuitive for learners
- Sequential IDs are user-friendly (1, 2, 3, ...)
- Performance is fine for 100+ todos
- Easy to extend to persistent storage in Phase II

**Alternatives Considered**:
- Dict-based storage: Rejected (unnecessary complexity for Phase I)
- UUID-based IDs: Rejected (not user-friendly for CLI)
- shelve module (disk persistence): Rejected (violates Phase I constraint)

---

## 6. Logging Strategy

### Decision: Python Logging Module with Structured Format

**Selected Approach**: Use standard library `logging` with JSON formatting

**Configuration**:
```python
import logging
import json
from datetime import datetime

class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_obj = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }
        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_obj)

def setup_logger() -> logging.Logger:
    logger = logging.getLogger("todo-cli")
    logger.setLevel(logging.DEBUG)

    # Console handler (human-readable for dev)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(
        logging.Formatter("%(levelname)s: %(message)s")
    )

    # File handler (JSON for production)
    file_handler = logging.FileHandler("todo-cli.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(JSONFormatter())

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
```

**Logging Best Practices**:
```python
# Log at appropriate levels
logger.debug("Processing todo ID: %d", todo_id)
logger.info("Created todo: %s", todo.description)
logger.warning("Todo not found: %d", todo_id)
logger.error("Invalid input: %s", error_message)

# Include context in logs
logger.info("Todo updated", extra={
    "todo_id": todo.id,
    "operation": "update",
    "user_input": description
})
```

**Rationale**:
- Standard library (no external dependencies)
- JSON format enables log aggregation in future phases
- Structured logs are machine-readable and queryable
- Meets constitution's observability requirement

**Alternatives Considered**:
- Print statements: Rejected (not production-grade, not structured)
- structlog: Rejected (external dependency)
- loguru: Rejected (external dependency)

---

## Summary

**All research questions resolved**:

1. ✅ **Python 3.13+ with UV**: pyproject.toml structure defined
2. ✅ **CLI Best Practices**: Menu-driven interface with input() and validation
3. ✅ **Clean Architecture**: Four-layer structure (domain/services/adapters/infrastructure)
4. ✅ **Type Safety**: mypy strict mode, ruff for linting
5. ✅ **In-Memory Storage**: List-based with sequential IDs
6. ✅ **Logging**: Python logging module with JSON formatting

**Key Technical Decisions**:
- UV for project management
- No external dependencies (only dev dependencies)
- Clean architecture with clear layer boundaries
- Type hints enforced with mypy strict mode
- Structured logging from the start

**Ready for Phase 1**: Design artifacts (data-model, contracts, quickstart)
