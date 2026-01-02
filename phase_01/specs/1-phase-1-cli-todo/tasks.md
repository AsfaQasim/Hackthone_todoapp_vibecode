# Tasks: Phase I In-Memory CLI Todo App

**Input**: Design documents from `/specs/1-phase-1-cli-todo/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/cli-interface.md

**Tests**: Constitution requires TDD approach. Tests are included for all user stories.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

**Single project structure** (from plan.md):
- Source: `src/` at repository root
- Tests: `tests/` at repository root
- Domain: `src/domain/`
- Services: `src/services/`
- Adapters: `src/adapters/`
- Infrastructure: `src/infrastructure/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project root directory structure (src/, tests/, src/domain/, src/services/, src/adapters/, src/infrastructure/)
- [x] T002 Initialize Python project with UV (uv init --name todo-cli --python 3.13)
- [x] T003 [P] Create pyproject.toml with dependencies (pytest, mypy, ruff as dev dependencies)
- [x] T004 [P] Create .python-version file specifying Python 3.13
- [x] T005 [P] Create .gitignore file for Python projects
- [x] T006 [P] Create __init__.py files in all package directories

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Implement Todo domain entity in src/domain/todo.py with validation
- [x] T008 [P] Implement TodoStorage protocol in src/infrastructure/storage.py
- [x] T009 [P] Implement InMemoryStorage implementation in src/infrastructure/storage.py
- [x] T010 [P] Implement logging configuration in src/infrastructure/logger.py with JSON formatting
- [x] T011 Implement TodoService in src/services/todo_service.py with dependency injection
- [x] T012 [P] Create unit tests for Todo entity in tests/unit/test_todo.py
- [x] T013 [P] Create unit tests for InMemoryStorage in tests/unit/test_storage.py
- [x] T014 [P] Create unit tests for TodoService in tests/unit/test_todo_service.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Create and View Todos (Priority: P1) 🎯 MVP

**Goal**: User can create new todo items and view them in a clear list format

**Independent Test**: Launch app, add one or more todos, view the list. Delivers immediate value as a basic task tracker.

### Tests for User Story 1 (TDD Approach)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T015 [P] [US1] Create integration test for add todo workflow in tests/integration/test_cli_workflows.py
- [x] T016 [P] [US1] Create integration test for view todos workflow in tests/integration/test_cli_workflows.py
- [x] T017 [P] [US1] Create integration test for empty list scenario in tests/integration/test_cli_workflows.py

### Implementation for User Story 1

- [x] T018 [US1] Implement main menu display function in src/adapters/cli.py
- [x] T019 [US1] Implement menu choice input and validation in src/adapters/cli.py
- [x] T020 [US1] Implement add todo command in src/adapters/cli.py (calls TodoService.create_todo)
- [x] T021 [US1] Implement view all todos command in src/adapters/cli.py (calls TodoService.get_all_todos)
- [x] T022 [US1] Implement todo list table formatting in src/adapters/cli.py
- [x] T023 [US1] Implement empty list message display in src/adapters/cli.py
- [x] T024 [US1] Add input validation for todo description in src/adapters/cli.py
- [x] T025 [US1] Add error handling and user-friendly error messages in src/adapters/cli.py
- [x] T026 [US1] Add logging for add and view operations in src/adapters/cli.py
- [x] T027 [US1] Create main entry point in src/main.py with dependency injection setup

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. Users can add and view todos.

---

## Phase 4: User Story 2 - Mark Todos Complete/Incomplete (Priority: P2)

**Goal**: User can mark todos as complete or incomplete to track progress

**Independent Test**: Create a todo, mark it complete, verify status changes. Mark it incomplete again, verify status reverts. Delivers task completion tracking.

### Tests for User Story 2 (TDD Approach)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T028 [P] [US2] Create integration test for mark complete workflow in tests/integration/test_cli_workflows.py
- [x] T029 [P] [US2] Create integration test for mark incomplete workflow in tests/integration/test_cli_workflows.py
- [x] T030 [P] [US2] Create integration test for non-existent ID error in tests/integration/test_cli_workflows.py

### Implementation for User Story 2

- [x] T031 [US2] Implement mark complete command in src/adapters/cli.py (calls TodoService.mark_complete)
- [x] T032 [US2] Implement mark incomplete command in src/adapters/cli.py (calls TodoService.mark_incomplete)
- [x] T033 [US2] Add ID input validation (numeric, positive) in src/adapters/cli.py
- [x] T034 [US2] Add error handling for non-existent todos in src/adapters/cli.py
- [x] T035 [US2] Add success messages for status changes in src/adapters/cli.py
- [x] T036 [US2] Add info messages for already complete/incomplete scenarios in src/adapters/cli.py
- [x] T037 [US2] Add logging for mark complete/incomplete operations in src/adapters/cli.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently. Users can add, view, and manage completion status.

---

## Phase 5: User Story 3 - Filter Todos by Status (Priority: P3)

**Goal**: User can filter todos to show only completed, only incomplete, or all todos

**Independent Test**: Create several todos with mixed statuses, apply each filter, verify correct todos shown. Delivers focused task views.

### Tests for User Story 3 (TDD Approach)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T038 [P] [US3] Create integration test for filter by complete in tests/integration/test_cli_workflows.py
- [x] T039 [P] [US3] Create integration test for filter by incomplete in tests/integration/test_cli_workflows.py
- [x] T040 [P] [US3] Create integration test for show all filter in tests/integration/test_cli_workflows.py

### Implementation for User Story 3

- [x] T041 [US3] Implement filter submenu display in src/adapters/cli.py
- [x] T042 [US3] Implement filter choice input and validation in src/adapters/cli.py
- [x] T043 [US3] Implement show all filter in src/adapters/cli.py (calls TodoService.get_all_todos)
- [x] T044 [US3] Implement show complete filter in src/adapters/cli.py (calls TodoService.get_completed_todos)
- [x] T045 [US3] Implement show incomplete filter in src/adapters/cli.py (calls TodoService.get_incomplete_todos)
- [x] T046 [US3] Add empty results messaging for each filter type in src/adapters/cli.py
- [x] T047 [US3] Add logging for filter operations in src/adapters/cli.py

**Checkpoint**: All user stories 1, 2, and 3 should now be independently functional. Users have full view and filter capabilities.

---

## Phase 6: User Story 4 - Update Todo Description (Priority: P4)

**Goal**: User can edit todo descriptions to correct typos or change details

**Independent Test**: Create a todo, update its description, verify the description changed. Delivers editing capability.

### Tests for User Story 4 (TDD Approach)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T048 [P] [US4] Create integration test for update todo workflow in tests/integration/test_cli_workflows.py
- [x] T049 [P] [US4] Create integration test for update with invalid ID in tests/integration/test_cli_workflows.py
- [x] T050 [P] [US4] Create integration test for update with empty description in tests/integration/test_cli_workflows.py

### Implementation for User Story 4

- [x] T051 [US4] Implement update todo command in src/adapters/cli.py (calls TodoService.update_todo)
- [x] T052 [US4] Add ID input and validation for update in src/adapters/cli.py
- [x] T053 [US4] Add new description input and validation in src/adapters/cli.py
- [x] T054 [US4] Add success message showing old and new description in src/adapters/cli.py
- [x] T055 [US4] Add error handling for non-existent todos and invalid descriptions in src/adapters/cli.py
- [x] T056 [US4] Add logging for update operations in src/adapters/cli.py

**Checkpoint**: User stories 1-4 complete. Users can create, view, filter, mark status, and edit todos.

---

## Phase 7: User Story 5 - Delete Todos (Priority: P5)

**Goal**: User can delete todos when no longer needed

**Independent Test**: Create a todo, delete it by ID, verify removed from list. Delivers list management.

### Tests for User Story 5 (TDD Approach)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T057 [P] [US5] Create integration test for delete todo workflow in tests/integration/test_cli_workflows.py
- [x] T058 [P] [US5] Create integration test for delete with confirmation in tests/integration/test_cli_workflows.py
- [x] T059 [P] [US5] Create integration test for delete cancellation in tests/integration/test_cli_workflows.py

### Implementation for User Story 5

- [x] T060 [US5] Implement delete todo command in src/adapters/cli.py (calls TodoService.delete_todo)
- [x] T061 [US5] Add ID input and validation for delete in src/adapters/cli.py
- [x] T062 [US5] Implement confirmation prompt (y/n) in src/adapters/cli.py
- [x] T063 [US5] Add confirmation input validation (accepts y/yes/n/no, case-insensitive) in src/adapters/cli.py
- [x] T064 [US5] Add success message showing deleted todo details in src/adapters/cli.py
- [x] T065 [US5] Add cancellation message when user declines in src/adapters/cli.py
- [x] T066 [US5] Add error handling for non-existent todos in src/adapters/cli.py
- [x] T067 [US5] Add logging for delete operations in src/adapters/cli.py

**Checkpoint**: All 5 user stories complete. Full CRUD functionality delivered.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T068 [P] Implement exit command in src/adapters/cli.py with goodbye message
- [x] T069 [P] Add keyboard interrupt handling (Ctrl+C) in src/main.py
- [x] T070 [P] Add comprehensive docstrings to all public functions in src/domain/todo.py
- [x] T071 [P] Add comprehensive docstrings to all public functions in src/services/todo_service.py
- [x] T072 [P] Add comprehensive docstrings to all public functions in src/adapters/cli.py
- [x] T073 [P] Add comprehensive docstrings to all public functions in src/infrastructure/storage.py
- [x] T074 [P] Run mypy type checking and fix all type errors (uv run mypy src/)
- [x] T075 [P] Run ruff linting and fix all issues (uv run ruff check src/ --fix)
- [x] T076 [P] Run all tests and ensure 80%+ coverage (uv run pytest --cov=src --cov-report=term-missing)
- [x] T077 Create README.md with project overview and link to quickstart
- [x] T078 Validate quickstart.md commands (manually test each command)
- [x] T079 Verify all success criteria from spec.md (manual testing checklist)
- [x] T080 Performance testing (startup time <2s, operations <5s, 100+ todos)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational phase completion
- **User Story 2 (Phase 4)**: Depends on Foundational phase completion (can run parallel with US1 if multiple developers)
- **User Story 3 (Phase 5)**: Depends on Foundational phase completion (can run parallel with US1/US2)
- **User Story 4 (Phase 6)**: Depends on Foundational phase completion (can run parallel with US1/US2/US3)
- **User Story 5 (Phase 7)**: Depends on Foundational phase completion (can run parallel with US1/US2/US3/US4)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

**All user stories are independently implementable after Foundational phase completes.**

- **User Story 1 (P1)**: No dependencies on other stories - Can start immediately after Foundational
- **User Story 2 (P2)**: No dependencies on other stories - Can start immediately after Foundational
- **User Story 3 (P3)**: No dependencies on other stories - Can start immediately after Foundational
- **User Story 4 (P4)**: No dependencies on other stories - Can start immediately after Foundational
- **User Story 5 (P5)**: No dependencies on other stories - Can start immediately after Foundational

**Key Insight**: After Foundational phase, ALL user stories can be developed in parallel by different team members, OR sequentially in priority order (P1 → P2 → P3 → P4 → P5) for single developer.

### Within Each User Story

**TDD Flow** (constitution requirement):
1. **Tests FIRST**: Write tests, ensure they FAIL
2. **Implementation**: Write minimal code to pass tests
3. **Refactor**: Clean up while keeping tests green

**Task Execution Order**:
- Tests (marked [P]) can run in parallel
- Implementation tasks run sequentially unless marked [P]
- Logging/error handling tasks depend on core implementation

### Parallel Opportunities

#### Phase 1 (Setup)
All tasks except T001 can run in parallel after directory structure created:
```bash
# After T001 completes:
Task: T002, T003, T004, T005, T006 (all parallel)
```

#### Phase 2 (Foundational)
Multiple parallel tracks:
```bash
# Track 1: Domain
Task: T007 (Todo entity)

# Track 2: Infrastructure (parallel)
Task: T008, T009, T010 (Storage and Logging - all parallel)

# Track 3: Service (depends on T007, T008)
Task: T011 (TodoService - after T007 and T008 complete)

# Track 4: Tests (depends on implementation)
Task: T012, T013, T014 (all parallel after T007, T009, T011 complete)
```

#### Phase 3 (User Story 1)
Tests can run in parallel:
```bash
# Tests (all parallel)
Task: T015, T016, T017

# Implementation (mostly sequential, some parallel opportunities)
Task: T018 (main menu)
Task: T019 (menu input)
Then parallel: T020, T021 (add and view commands)
Task: T022, T023 (formatting)
Then parallel: T024, T025, T026, T027
```

#### Phase 4-7 (User Stories 2-5)
Each user story's tests can run in parallel:
```bash
# User Story 2 Tests (parallel)
Task: T028, T029, T030

# User Story 3 Tests (parallel)
Task: T038, T039, T040

# User Story 4 Tests (parallel)
Task: T048, T049, T050

# User Story 5 Tests (parallel)
Task: T057, T058, T059
```

#### Phase 8 (Polish)
Most tasks are independent and can run in parallel:
```bash
# Parallel track 1: Documentation
Task: T068, T069, T070, T071, T072, T073, T077

# Parallel track 2: Quality checks
Task: T074, T075, T076

# Sequential: Final validation
Task: T078, T079, T080 (manual testing, sequential)
```

---

## Parallel Example: Foundational Phase

```bash
# Launch domain entity development
Task: "Implement Todo domain entity in src/domain/todo.py"

# Launch infrastructure development (parallel with domain)
Task: "Implement TodoStorage protocol in src/infrastructure/storage.py"
Task: "Implement InMemoryStorage in src/infrastructure/storage.py"
Task: "Implement logging configuration in src/infrastructure/logger.py"

# After Todo entity and TodoStorage complete:
Task: "Implement TodoService in src/services/todo_service.py"

# After all implementations complete, launch tests (all parallel):
Task: "Create unit tests for Todo entity in tests/unit/test_todo.py"
Task: "Create unit tests for InMemoryStorage in tests/unit/test_storage.py"
Task: "Create unit tests for TodoService in tests/unit/test_todo_service.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only) - RECOMMENDED FOR LEARNING

**Fastest path to working app**:

1. Complete Phase 1: Setup (T001-T006)
2. Complete Phase 2: Foundational (T007-T014) - CRITICAL BLOCKER
3. Complete Phase 3: User Story 1 (T015-T027)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. **DEMO**: Show working todo app (add + view)

**Result**: Working MVP in ~20 tasks. Users can add and view todos.

**Time Estimate**: 2-3 hours for experienced developer, 4-6 hours for learner

---

### Incremental Delivery (Priority Order)

**Each increment adds value**:

1. **Setup + Foundational** → Foundation ready (T001-T014)
2. **Add User Story 1** → Test independently → Demo (add + view) [MVP!]
3. **Add User Story 2** → Test independently → Demo (mark complete/incomplete)
4. **Add User Story 3** → Test independently → Demo (filtering)
5. **Add User Story 4** → Test independently → Demo (editing)
6. **Add User Story 5** → Test independently → Demo (deletion)
7. **Polish** → Production ready

**Benefits**:
- Each story delivers independent value
- Can stop at any point and have working app
- Early feedback possible after each story
- Risk reduced (working software at each stage)

---

### Parallel Team Strategy (If Multiple Developers)

**With 3+ developers**:

**Week 1**:
- **Team**: Complete Setup + Foundational together (T001-T014)

**Week 2** (after Foundational complete):
- **Developer A**: User Story 1 (T015-T027)
- **Developer B**: User Story 2 (T028-T037)
- **Developer C**: User Story 3 (T038-T047)

**Week 3**:
- **Developer A**: User Story 4 (T048-T056)
- **Developer B**: User Story 5 (T057-T067)
- **Developer C**: Polish (T068-T080)

**Result**: All stories complete in 3 weeks with parallel development

---

## Test-First Workflow (TDD - Constitution Requirement)

**For each user story**:

```bash
# 1. Write tests FIRST (RED phase)
uv run pytest tests/integration/test_cli_workflows.py
# Expected: FAIL (tests for unimplemented feature)

# 2. Implement minimal code (GREEN phase)
# Write just enough code to make tests pass
uv run pytest tests/integration/test_cli_workflows.py
# Expected: PASS

# 3. Refactor (REFACTOR phase)
# Clean up code while keeping tests green
uv run pytest tests/integration/test_cli_workflows.py
# Expected: PASS (still passing after refactor)

# 4. Type check and lint
uv run mypy src/
uv run ruff check src/

# 5. Commit
git add .
git commit -m "Implement User Story X: <description>"
```

---

## Quality Gates

### Before Starting Implementation

- ✅ All design documents reviewed (plan.md, spec.md, data-model.md, contracts/)
- ✅ Constitution check passed (from plan.md)
- ✅ Development environment setup (Python 3.13+, UV installed)

### After Foundational Phase (GATE)

**CRITICAL CHECKPOINT** - Must pass before any user story work:

- ✅ Todo entity implemented with full validation
- ✅ InMemoryStorage working (all CRUD operations)
- ✅ TodoService implemented with dependency injection
- ✅ Logging configured and working
- ✅ All foundational unit tests passing (T012-T014)
- ✅ Type checking passing (mypy)
- ✅ Linting passing (ruff)

### After Each User Story

- ✅ Story-specific tests written FIRST and initially FAIL
- ✅ Implementation makes tests PASS
- ✅ Independent test criteria verified (from spec.md)
- ✅ Type checking passing (mypy src/)
- ✅ Linting passing (ruff check src/)
- ✅ Code reviewed for clean architecture
- ✅ Logging instrumented for story operations

### Before Completion (Final Gate)

- ✅ All user stories implemented (P1-P5)
- ✅ All tests passing (uv run pytest)
- ✅ Test coverage ≥ 80% (uv run pytest --cov=src)
- ✅ Type checking passing (uv run mypy src/)
- ✅ Linting passing (uv run ruff check src/)
- ✅ All quickstart.md commands work (manual validation)
- ✅ All success criteria verified (from spec.md)
- ✅ No TODO comments or placeholders in code
- ✅ All docstrings complete
- ✅ Performance verified (startup <2s, operations <5s)

---

## Success Criteria Validation (from spec.md)

**How to verify each success criterion**:

1. **SC-001** (Create todo <5s):
   ```bash
   # Time manually: Launch app, add todo, check list
   time uv run python -m src.main
   # Verify operation completes in <5 seconds
   ```

2. **SC-002** (No errors/crashes):
   ```bash
   # Run all CRUD operations, no exceptions
   uv run python -m src.main
   # Try: add, view, mark complete, filter, update, delete
   # Expected: No crashes, clean exit
   ```

3. **SC-003** (Full workflow <2 min):
   ```bash
   # Time manually: add 3, mark 1 complete, filter, update 1, delete 1
   time uv run python -m src.main
   # Follow workflow, verify <2 minutes total
   ```

4. **SC-004** (Clear feedback):
   ```bash
   # Verify every action shows success/error message
   # Check: ✓ for success, ✗ for error, ℹ️ for info
   ```

5. **SC-005** (100% user-friendly errors):
   ```bash
   # Test all invalid inputs
   # Try: empty description, invalid ID, non-numeric, non-existent ID
   # Expected: User-friendly errors, no crashes
   ```

6. **SC-006** (Startup <2s):
   ```bash
   time uv run python -m src.main
   # Verify app ready in <2 seconds
   ```

7. **SC-007** (Readable output):
   ```bash
   # Visual inspection of list formatting
   # Check: aligned columns, clear spacing, readable table
   ```

---

## Notes

- **[P] tasks**: Different files, no dependencies - can run in parallel
- **[Story] labels**: Map tasks to user stories for traceability
- **TDD Required**: Constitution mandates test-first approach
- **Independent Stories**: Each user story is fully testable on its own after Foundational phase
- **MVP = User Story 1**: Fastest path to working app (add + view only)
- **Commit Strategy**: Commit after each task or logical group
- **Stop at Checkpoints**: Validate story independently before proceeding
- **No Shortcuts**: All quality gates must pass (type checking, linting, tests)

**Total Tasks**: 80
- Setup: 6 tasks
- Foundational: 8 tasks (BLOCKER for all stories)
- User Story 1: 13 tasks (MVP)
- User Story 2: 10 tasks
- User Story 3: 10 tasks
- User Story 4: 9 tasks
- User Story 5: 11 tasks
- Polish: 13 tasks

**Parallel Opportunities**: 40+ tasks marked [P] (can run in parallel when dependencies met)

**MVP Scope**: 27 tasks (Setup + Foundational + US1) = Working todo app with add + view
