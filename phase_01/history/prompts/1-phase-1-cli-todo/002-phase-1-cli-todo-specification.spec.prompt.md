---
id: 002
title: Phase I CLI Todo Specification
stage: spec
date: 2026-01-02
surface: agent
model: claude-sonnet-4-5
feature: 1-phase-1-cli-todo
branch: 1-phase-1-cli-todo
user: unknown
command: /sp.specify
labels: ["spec", "phase-1", "cli", "todo-app", "python"]
links:
  spec: specs/1-phase-1-cli-todo/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/1-phase-1-cli-todo/spec.md
 - specs/1-phase-1-cli-todo/checklists/requirements.md
tests:
 - N/A
---

## Prompt

/sp.specify Phase I In-Memory CLI Todo App

Target audience:
Python learners using Claude Code and Spec-Kit Plus

Objective:
Build a command-line Todo app that stores tasks in memory using Python 3.13+.

Success criteria:
- Add, view, update, delete todos
- Mark todos as complete/incomplete
- Clean CLI output and input handling
- Runs via `uv run` without errors

Constraints:
- In-memory only (no files, no database)
- Python 3.13+
- Tools: UV, Claude Code, Spec-Kit Plus
- Modular, clean Python project structure

Not building:
- Persistence
- Web/UI
- AI or chatbot features
- Advanced todo features

## Response snapshot

Created comprehensive feature specification for Phase I In-Memory CLI Todo App:

**Branch**: 1-phase-1-cli-todo
**Spec File**: specs/1-phase-1-cli-todo/spec.md

**User Stories (5 prioritized, independently testable)**:
- P1: Create and View Todos (foundation - add and list)
- P2: Mark Complete/Incomplete (core value - track progress)
- P3: Filter by Status (usability - focused views)
- P4: Update Todo Description (nice-to-have - editing)
- P5: Delete Todos (cleanup - list management)

**Functional Requirements**: 14 requirements covering CRUD operations, validation, error handling, and in-memory storage

**Success Criteria**: 7 measurable, technology-agnostic outcomes:
- Performance: Create todo in <5s, startup in <2s
- Reliability: 100% error-free CRUD operations
- Usability: Full workflow in <2 minutes, clear feedback for all actions
- Quality: User-friendly error messages, formatted output

**Key Entity**: Todo (ID, Description, Status)

**Validation**: All 20 checklist items passed ✅
- No implementation details (stays at user/business level)
- No [NEEDS CLARIFICATION] markers (all requirements concrete)
- All scenarios, edge cases, assumptions documented
- Ready for `/sp.plan`

**Assumptions**: Single user, session-based (no persistence), English UI, standard CLI patterns

**Non-Goals**: Persistence, web UI, AI features, multi-user, advanced organization

## Outcome

- ✅ Impact: Complete, validated specification for Phase I CLI Todo App. All 5 user stories independently testable. Foundation for Phase II web app.
- 🧪 Tests: N/A (specification document)
- 📁 Files: Created specs/1-phase-1-cli-todo/spec.md and checklists/requirements.md
- 🔁 Next prompts: `/sp.plan` to create implementation plan, or `/sp.clarify` if additional questions arise (though none needed)
- 🧠 Reflection: Specification successfully balances simplicity for Phase I (in-memory CLI) while setting foundation for future phases. Clear prioritization enables MVP-first approach (P1 only = viable product).

## Evaluation notes (flywheel)

- Failure modes observed: None - specification passed all validation criteria on first iteration
- Graders run and results (PASS/FAIL): Spec Quality Checklist - 20/20 items PASSED
- Prompt variant (if applicable): Standard spec template with constitution-aligned structure
- Next experiment (smallest change to try): Validate that planning phase (sp.plan) successfully translates spec into Python 3.13+ implementation approach
