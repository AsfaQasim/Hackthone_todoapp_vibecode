# Quickstart Guide: Phase I In-Memory CLI Todo App

**Date**: 2026-01-02
**Feature**: Phase I In-Memory CLI Todo App
**Purpose**: Get the app running in under 5 minutes

## Prerequisites

**Required**:
- Python 3.13 or higher
- UV (modern Python package manager)

**Check versions**:
```bash
python --version  # Should show Python 3.13.x
uv --version      # Should show uv version
```

**Install UV** (if not installed):
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Quick Start (3 Steps)

### 1. Clone and Navigate

```bash
cd phase_01
```

### 2. Setup Project

```bash
# Initialize project with UV (first time only)
uv init --name todo-cli --python 3.13

# Install dependencies
uv sync
```

### 3. Run the Application

```bash
# Run the app
uv run python -m src.main

# Alternative: shorter command
uv run todo-cli
```

**Expected Output**:
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

Enter your choice (1-8):
```

## Basic Usage

### Create Your First Todo

1. Launch the app: `uv run python -m src.main`
2. Select option `1` (Add Todo)
3. Enter description: `Buy groceries`
4. Press Enter

**Result**: Todo created with ID 1

### View Your Todos

1. From main menu, select option `2` (View All Todos)
2. See your todo listed with ID, status, and description

### Mark Todo Complete

1. From main menu, select option `4` (Mark Todo Complete)
2. Enter the todo ID: `1`
3. Press Enter

**Result**: Todo marked as complete ✓

### Filter Todos

1. From main menu, select option `3` (Filter Todos)
2. Select filter:
   - Option `1`: Show all todos
   - Option `2`: Show complete only
   - Option `3`: Show incomplete only
3. See filtered results

### Update Todo Description

1. From main menu, select option `6` (Update Todo)
2. Enter todo ID: `1`
3. Enter new description: `Buy groceries and milk`
4. Press Enter

**Result**: Description updated

### Delete Todo

1. From main menu, select option `7` (Delete Todo)
2. Enter todo ID: `1`
3. Confirm deletion: `y`

**Result**: Todo permanently deleted

### Exit Application

1. From main menu, select option `8` (Exit)
2. Application closes gracefully

**Note**: All data is lost on exit (in-memory only)

## Development Commands

### Run Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src --cov-report=term-missing

# Run specific test file
uv run pytest tests/unit/test_todo.py

# Run with verbose output
uv run pytest -v
```

### Type Checking

```bash
# Check all source files
uv run mypy src/

# Check specific file
uv run mypy src/domain/todo.py
```

### Linting

```bash
# Check code style
uv run ruff check src/

# Auto-fix issues
uv run ruff check src/ --fix

# Check tests too
uv run ruff check src/ tests/
```

### Format Code

```bash
# Format all Python files
uv run ruff format src/ tests/
```

## Project Structure

```
phase_01/
├── src/                    # Source code
│   ├── main.py             # Entry point
│   ├── domain/             # Business entities
│   │   └── todo.py
│   ├── services/           # Business logic
│   │   └── todo_service.py
│   ├── adapters/           # CLI interface
│   │   └── cli.py
│   └── infrastructure/     # Storage & logging
│       ├── storage.py
│       └── logger.py
├── tests/                  # Test suite
│   ├── unit/               # Unit tests
│   └── integration/        # Integration tests
├── pyproject.toml          # Project config
├── .python-version         # Python version
└── README.md               # Documentation
```

## Configuration

### Environment Variables (Optional)

```bash
# Set log level (default: INFO)
export TODO_LOG_LEVEL=DEBUG

# Set log file (default: todo-cli.log)
export TODO_LOG_FILE=my-custom.log
```

### pyproject.toml

```toml
[project]
name = "todo-cli"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = []

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "mypy>=1.8.0",
    "ruff>=0.1.0",
]

[project.scripts]
todo-cli = "src.main:main"
```

## Troubleshooting

### Issue: "python: command not found"

**Solution**: Install Python 3.13+
```bash
# Check if python3 works instead
python3 --version

# If yes, use python3 instead of python
uv run python3 -m src.main
```

### Issue: "uv: command not found"

**Solution**: Install UV (see Prerequisites above)

### Issue: "Module 'src' not found"

**Solution**: Run from project root (phase_01/)
```bash
# Make sure you're in the right directory
pwd  # Should show .../phase_01

# If not, navigate there
cd phase_01
```

### Issue: Type errors when running mypy

**Solution**: Ensure all type hints are correct
```bash
# Run mypy with verbose output
uv run mypy src/ --show-error-codes

# Fix reported issues in source files
```

### Issue: App crashes on invalid input

**Solution**: This should not happen! Please report as bug.
```bash
# Run with debug logging to see what happened
export TODO_LOG_LEVEL=DEBUG
uv run python -m src.main

# Check log file
cat todo-cli.log
```

### Issue: Tests failing

**Solution**: Check test output for details
```bash
# Run with verbose and capture disabled
uv run pytest -v -s

# Run single failing test
uv run pytest tests/unit/test_todo.py::test_name -v
```

## Performance Expectations

**Startup Time**: <2 seconds
**Operation Response**: <5 seconds per action
**Capacity**: 100+ todos without slowdown
**Memory Usage**: <50 MB

## Limitations (Phase I)

**No Persistence**:
- All data lost on exit
- No save/load functionality
- Session-based only

**No Multi-User**:
- Single user only
- No authentication
- No concurrent access

**No Network**:
- Offline only
- No sync capabilities
- No remote storage

**Future Phases** will add:
- Phase II: Web UI with persistence (PostgreSQL)
- Phase III: AI conversational interface
- Phase IV: Kubernetes deployment
- Phase V: Cloud-native with Kafka/Dapr

## Success Criteria Checklist

Verify app meets all success criteria:

- [ ] **SC-001**: Create todo and see it in list within 5 seconds
- [ ] **SC-002**: All CRUD operations work without errors
- [ ] **SC-003**: Full workflow (add 3, mark 1 complete, filter, update 1, delete 1) takes <2 minutes
- [ ] **SC-004**: Every action shows clear feedback (success/error messages)
- [ ] **SC-005**: Invalid inputs show user-friendly errors (no crashes)
- [ ] **SC-006**: App starts and is ready within 2 seconds
- [ ] **SC-007**: Output is clearly formatted and readable

**How to Verify**:
```bash
# Time startup
time uv run python -m src.main

# Test full workflow (manual timing)
# 1. Add 3 todos
# 2. Mark 1 complete
# 3. Filter by status
# 4. Update 1 description
# 5. Delete 1 todo

# Test error handling
# - Try empty description
# - Try invalid ID
# - Try non-numeric input
```

## Next Steps

**After running Phase I**:
1. ✅ Verify all success criteria met
2. ✅ Run full test suite (`uv run pytest`)
3. ✅ Check code quality (`uv run mypy src/ && uv run ruff check src/`)
4. ✅ Review logs (`cat todo-cli.log`)

**Ready for Phase II**:
- Add REST API with FastAPI
- Add persistence with PostgreSQL (Neon DB)
- Add frontend with Next.js

## Support

**Documentation**:
- [spec.md](./spec.md) - Feature specification
- [plan.md](./plan.md) - Implementation plan
- [data-model.md](./data-model.md) - Entity definitions
- [contracts/cli-interface.md](./contracts/cli-interface.md) - CLI interface details

**Getting Help**:
- Check troubleshooting section above
- Review log file: `todo-cli.log`
- Run tests to identify issues: `uv run pytest -v`
- Enable debug logging: `export TODO_LOG_LEVEL=DEBUG`

## Example Session

```bash
# Complete example session
$ cd phase_01
$ uv run python -m src.main

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

Enter todo description: Learn Python clean architecture

✓ Todo added successfully!
  ID: 1
  Description: Learn Python clean architecture
  Status: Incomplete

=== Todo CLI ===
...

Enter your choice (1-8): 2

=== All Todos ===

ID | Status      | Description
---|-------------|------------------------------------------
1  | Incomplete  | Learn Python clean architecture

Total: 1 todo (0 complete, 1 incomplete)

=== Todo CLI ===
...

Enter your choice (1-8): 4

Enter todo ID to mark complete: 1

✓ Todo marked as complete!
  ID: 1
  Description: Learn Python clean architecture
  Status: Complete

=== Todo CLI ===
...

Enter your choice (1-8): 8

Thank you for using Todo CLI! Goodbye.
```

## Notes

- First time setup takes ~1 minute (UV downloads dependencies)
- Subsequent runs take <2 seconds (dependencies cached)
- All commands are copy-paste ready (tested on macOS, Linux, Windows)
- Log file created automatically: `todo-cli.log`
