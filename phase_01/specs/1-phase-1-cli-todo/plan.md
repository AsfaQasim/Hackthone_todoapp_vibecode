# Implementation Plan: Phase I In-Memory CLI Todo App

**Branch**: `1-phase-1-cli-todo` | **Date**: 2026-01-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/1-phase-1-cli-todo/spec.md`

## Summary

Build a command-line Todo application in Python 3.13+ that stores tasks in memory. Target audience is Python learners using Claude Code and Spec-Kit Plus. The app provides CRUD operations (create, read, update, delete) for todos, status management (complete/incomplete), and filtering capabilities. All data is stored in memory only (no persistence). The CLI provides a clear menu-driven interface with proper input validation and error handling.

**Technical Approach**: Clean architecture with separation of concerns - domain layer (Todo entity with validation), service layer (CRUD operations, business logic), adapter layer (CLI interface), and infrastructure layer (in-memory storage, logging). Sequential ID generation, input validation with user-friendly error messages, and structured logging for observability.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**:
- Standard library only (no external dependencies for core functionality)
- pytest (testing framework, dev dependency)
- mypy or pyright (type checking, dev dependency)
- ruff or pylint (linting, dev dependency)

**Storage**: In-memory only (Python list data structure)
**Testing**: pytest with unit tests for all CRUD operations
**Target Platform**: Cross-platform CLI (Windows, macOS, Linux)
**Project Type**: Single project (CLI application)
**Performance Goals**:
- App startup: <2 seconds
- Operation response time: <5 seconds per action
- Support for 100+ todos without performance degradation

**Constraints**:
- No persistence (in-memory only)
- No external dependencies for core app (only dev dependencies)
- Single-user, single-session usage
- Standard input/output only
- UTF-8 character encoding

**Scale/Scope**:
- Learning project (Python learners)
- 100-500 lines of production code
- 5 user stories (P1-P5)
- 14 functional requirements

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### I. Incremental Architecture ✅
- **Status**: PASS
- **Rationale**: Phase I establishes foundation for Phase II (web app). Domain and service layers designed to be reusable when adding REST API adapter in Phase II.

### II. Production-Grade from Day One ✅
- **Status**: PASS
- **Requirements**:
  - ✅ Type hints required (enforced via mypy/pyright)
  - ✅ Explicit error handling (no silent failures)
  - ✅ Logging enabled (Python logging module)
  - ✅ Linting enforced (ruff/pylint)
  - ✅ No placeholder logic in delivered code

### III. Clear Separation of Concerns ✅
- **Status**: PASS
- **Layer Structure**:
  - **Domain** (`src/domain/todo.py`): Todo entity, validation rules
  - **Services** (`src/services/todo_service.py`): CRUD operations, business logic
  - **Adapters** (`src/adapters/cli.py`): CLI interface, user I/O
  - **Infrastructure** (`src/infrastructure/storage.py`, `src/infrastructure/logger.py`): In-memory storage, logging

### IV. Reproducibility & Determinism ✅
- **Status**: PASS
- **Requirements**:
  - ✅ `uv run` command documented in quickstart.md
  - ✅ All dependencies pinned in pyproject.toml
  - ✅ Copy-paste executable commands
  - ✅ No manual configuration required

### V. Observability & Scalability Readiness ✅
- **Status**: PASS
- **Requirements**:
  - ✅ Structured logging (Python logging module with JSON formatting)
  - ✅ Log levels (DEBUG, INFO, WARN, ERROR)
  - ✅ Critical paths instrumented (CRUD operations logged)
  - ✅ Errors logged with context (operation, inputs)

### VI. Security-First Design ✅
- **Status**: PASS
- **Requirements**:
  - ✅ Input validation at CLI boundary (no injection attacks)
  - ✅ No hardcoded credentials (N/A for Phase I)
  - ✅ No external services (N/A for Phase I)

### Phase I Specific Constraints ✅
- **Status**: PASS
- **Requirements**:
  - ✅ Python 3.13+
  - ✅ No database (in-memory lists only)
  - ✅ No external services
  - ✅ CLI UX clear and user-friendly
  - ✅ Unit tests required (pytest)
  - ✅ Test coverage ≥ 80% target

**Constitution Check Result**: ✅ ALL GATES PASSED

## Project Structure

### Documentation (this feature)

```text
specs/1-phase-1-cli-todo/
├── plan.md              # This file (/sp.plan command output)
├── spec.md              # Feature specification
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── cli-interface.md # CLI command interface specification
├── checklists/
│   └── requirements.md  # Specification validation checklist
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Single project structure (CLI application)

# Project root files
pyproject.toml           # Project metadata, dependencies (uv format)
.python-version          # Python version specification (3.13)
README.md                # Setup and usage instructions
.gitignore               # Git ignore rules

# Source code
src/
├── __init__.py
├── main.py              # Application entry point (CLI runner)
├── domain/              # Domain layer (business entities)
│   ├── __init__.py
│   └── todo.py          # Todo entity with validation
├── services/            # Service layer (business logic)
│   ├── __init__.py
│   └── todo_service.py  # CRUD operations, business rules
├── adapters/            # Adapter layer (external interfaces)
│   ├── __init__.py
│   └── cli.py           # CLI interface, menu, user I/O
└── infrastructure/      # Infrastructure layer (cross-cutting)
    ├── __init__.py
    ├── storage.py       # In-memory storage implementation
    └── logger.py        # Logging configuration

# Tests
tests/
├── __init__.py
├── unit/                # Unit tests (isolated)
│   ├── __init__.py
│   ├── test_todo.py     # Todo entity tests
│   ├── test_todo_service.py  # Service layer tests
│   └── test_storage.py  # Storage tests
└── integration/         # Integration tests (end-to-end)
    ├── __init__.py
    └── test_cli_workflows.py  # CLI workflow tests
```

**Structure Decision**: Single project structure selected because this is a standalone CLI application. The clean architecture with four layers (domain, services, adapters, infrastructure) enables Phase II extension by adding a REST API adapter alongside the CLI adapter without modifying domain or service layers.

**Rationale**:
- Domain layer is framework-agnostic and reusable
- Service layer contains all business logic (testable in isolation)
- Adapter layer (CLI) is swappable (Phase II adds REST API adapter)
- Infrastructure layer handles cross-cutting concerns (storage, logging)

## Complexity Tracking

> No constitution violations - this section intentionally left empty.

## Phase 0: Research & Technology Selection

### Research Questions

1. **Python 3.13+ Project Setup with UV**
   - How to initialize a Python 3.13+ project using UV?
   - What is the pyproject.toml structure for UV projects?
   - How to specify dev vs. production dependencies?

2. **CLI Best Practices in Python**
   - Menu-driven CLI patterns in Python standard library
   - Input validation and error handling patterns
   - User-friendly error message design

3. **Clean Architecture in Python**
   - Folder structure for domain/services/adapters/infrastructure
   - Dependency injection patterns in Python
   - Testing strategies for each layer

4. **Type Safety and Linting**
   - mypy vs. pyright: which to use for Python 3.13+?
   - ruff vs. pylint: modern linting tool selection
   - Type hint best practices for Python 3.13+

5. **In-Memory Storage Patterns**
   - Thread-safe in-memory storage (if needed for future)
   - ID generation strategies (sequential IDs)
   - Data structure selection (list vs. dict)

### Research Outputs

See [research.md](./research.md) for detailed findings.

## Phase 1: Design & Contracts

### Design Artifacts

1. **Data Model** ([data-model.md](./data-model.md))
   - Todo entity schema
   - Validation rules
   - State transitions (incomplete ↔ complete)

2. **CLI Interface Contract** ([contracts/cli-interface.md](./contracts/cli-interface.md))
   - Menu structure
   - Command list
   - Input/output formats
   - Error message catalog

3. **Quickstart Guide** ([quickstart.md](./quickstart.md))
   - Setup instructions (uv install)
   - Run commands (uv run)
   - Usage examples
   - Troubleshooting

### Architecture Decisions

**Decision 1: In-Memory Storage Implementation**
- **Choice**: Python list with sequential ID generation
- **Rationale**: Simple, sufficient for Phase I, easy to understand for learners
- **Alternatives Considered**: Dict-based storage (rejected - unnecessary complexity)

**Decision 2: CLI Interface Pattern**
- **Choice**: Menu-driven interface with numbered options
- **Rationale**: User-friendly for learners, clear action discovery
- **Alternatives Considered**: Command-line arguments (rejected - less discoverable)

**Decision 3: Type Checking Tool**
- **Choice**: mypy (standard, well-documented)
- **Rationale**: Industry standard, good error messages, Python 3.13+ support
- **Alternatives Considered**: pyright (rejected - less common in learning materials)

**Decision 4: Linting Tool**
- **Choice**: ruff (fast, modern, comprehensive)
- **Rationale**: Fastest Python linter, combines multiple tools, good defaults
- **Alternatives Considered**: pylint (rejected - slower, more verbose config)

**Decision 5: Logging Format**
- **Choice**: Structured logging with Python logging module
- **Rationale**: Standard library, JSON formatting for observability, no external deps
- **Alternatives Considered**: Print statements (rejected - not production-grade)

## Implementation Workflow

### Phase 2: Task Generation (Next Step)

Run `/sp.tasks` to generate detailed implementation tasks based on this plan.

**Expected task phases**:
1. **Setup**: Project initialization, folder structure, pyproject.toml
2. **Foundational**: Domain entities, infrastructure (storage, logging)
3. **User Story 1 (P1)**: Create and view todos
4. **User Story 2 (P2)**: Mark complete/incomplete
5. **User Story 3 (P3)**: Filter by status
6. **User Story 4 (P4)**: Update description
7. **User Story 5 (P5)**: Delete todos
8. **Polish**: Documentation, final testing, quickstart validation

### Testing Strategy

**Unit Tests** (tests/unit/):
- Todo entity validation
- Service layer CRUD operations
- Storage operations
- Input validation functions

**Integration Tests** (tests/integration/):
- Complete CLI workflows (add → view → mark complete → filter → delete)
- Error handling paths
- Edge cases from spec

**Test Coverage Target**: ≥ 80%

**Test-First Approach**: For constitution compliance, tests should be written first (TDD):
1. Write failing tests for a user story
2. Implement minimal code to pass tests
3. Refactor while keeping tests green

### Quality Gates

**Before Implementation**:
- ✅ Constitution check passed
- ✅ All research questions resolved
- ✅ Data model defined
- ✅ Contracts specified

**During Implementation** (per user story):
- ✅ Tests written and failing
- ✅ Implementation passes tests
- ✅ Type hints present (mypy passes)
- ✅ Linting passes (ruff)
- ✅ Code reviewed for clean architecture

**Before Completion**:
- ✅ All user stories implemented
- ✅ Test coverage ≥ 80%
- ✅ quickstart.md validated (commands work)
- ✅ No TODOs or placeholders in code
- ✅ Logging instrumented

## Success Criteria Validation

**How to verify each success criterion from spec**:

- **SC-001** (Create todo in <5s): Time the operation manually
- **SC-002** (No errors/crashes): Run all CRUD operations, no exceptions
- **SC-003** (Full workflow <2 min): Time the complete workflow
- **SC-004** (Clear feedback): Verify all operations show success/error messages
- **SC-005** (100% user-friendly errors): Test all invalid inputs, no crashes
- **SC-006** (Startup <2s): Time `uv run` command
- **SC-007** (Readable output): Visual inspection of list formatting

## Next Steps

1. **Review this plan** - Ensure technical approach aligns with constitution and spec
2. **Generate research.md** - Phase 0 research output (created next)
3. **Generate design artifacts** - Phase 1 outputs (data-model.md, contracts/, quickstart.md)
4. **Run `/sp.tasks`** - Generate detailed implementation tasks
5. **Run `/sp.implement`** - Execute tasks and build the application

## Notes

- This is Phase I of a multi-phase project (see constitution for full roadmap)
- Architecture designed to support Phase II (web app) without rewrites
- Focus on learning: code should be readable, well-documented, and exemplary for Python learners
- No premature optimization: simple solutions preferred over clever ones
