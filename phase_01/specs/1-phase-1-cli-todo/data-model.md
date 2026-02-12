# Data Model: Phase I In-Memory CLI Todo App

**Date**: 2026-01-02
**Feature**: Phase I In-Memory CLI Todo App
**Purpose**: Define entities, validation rules, and state transitions

## Entities

### Todo

**Description**: Represents a single task to be completed

**Attributes**:

| Attribute    | Type   | Required | Default   | Constraints                                    |
|--------------|--------|----------|-----------|------------------------------------------------|
| id           | int    | Yes      | Auto      | Unique, sequential, starts at 1                |
| description  | str    | Yes      | N/A       | 1-500 characters, non-empty after trim         |
| completed    | bool   | Yes      | False     | True (complete) or False (incomplete)          |

**Validation Rules**:

1. **Description Validation**:
   - MUST NOT be empty after trimming whitespace
   - MUST be between 1 and 500 characters after trimming
   - Special characters allowed (UTF-8)
   - Leading/trailing whitespace MUST be trimmed before storage

2. **ID Validation**:
   - MUST be positive integer (>0)
   - MUST be unique across all todos
   - MUST be auto-assigned (user cannot specify)
   - MUST be sequential (1, 2, 3, ...)
   - MUST NOT be reused after deletion

3. **Completed Validation**:
   - MUST be boolean (True or False)
   - MUST default to False on creation

**State Transitions**:

```
[New Todo]
    |
    v
[Incomplete] (completed = False)
    |
    |-- mark_complete() -->  [Complete] (completed = True)
    |                            |
    |                            |
    |<-- mark_incomplete() ------+
    |
    v
[Deleted] (removed from storage)
```

**State Transition Rules**:
- New todos start in Incomplete state (completed = False)
- Todos can transition between Incomplete ↔ Complete any number of times
- Deleted todos cannot be restored (permanent deletion)
- All state transitions MUST be logged

**Business Rules**:

1. **Creation**:
   - Description MUST be provided
   - ID is auto-assigned (next available sequential number)
   - Initial state is always Incomplete (completed = False)

2. **Update**:
   - Only description can be updated
   - ID MUST NOT change
   - Completed status is changed via separate mark operations
   - Updated description MUST pass same validation as creation

3. **Status Change**:
   - Can mark complete: Incomplete → Complete
   - Can mark incomplete: Complete → Incomplete
   - Can toggle status repeatedly

4. **Deletion**:
   - Todo is permanently removed from storage
   - ID is NOT reused for future todos
   - Deletion MUST succeed even if todo is Complete

## Python Implementation

### Domain Entity

```python
from dataclasses import dataclass
from typing import ClassVar

@dataclass
class Todo:
    """
    Domain entity representing a todo item.

    Attributes:
        id: Unique identifier (auto-assigned)
        description: Task description (1-500 chars after trim)
        completed: Completion status (False = incomplete, True = complete)
    """

    id: int
    description: str
    completed: bool = False

    # Class-level constants
    MAX_DESCRIPTION_LENGTH: ClassVar[int] = 500
    MIN_DESCRIPTION_LENGTH: ClassVar[int] = 1

    def __post_init__(self) -> None:
        """Validate todo attributes after initialization."""
        self._validate_description()
        self._validate_id()

    def _validate_description(self) -> None:
        """Validate description field."""
        if not isinstance(self.description, str):
            raise TypeError("Description must be a string")

        trimmed = self.description.strip()

        if not trimmed:
            raise ValueError("Description cannot be empty or whitespace-only")

        if len(trimmed) < self.MIN_DESCRIPTION_LENGTH:
            raise ValueError(
                f"Description must be at least {self.MIN_DESCRIPTION_LENGTH} character"
            )

        if len(trimmed) > self.MAX_DESCRIPTION_LENGTH:
            raise ValueError(
                f"Description cannot exceed {self.MAX_DESCRIPTION_LENGTH} characters"
            )

        # Store trimmed version
        self.description = trimmed

    def _validate_id(self) -> None:
        """Validate ID field."""
        if not isinstance(self.id, int):
            raise TypeError("ID must be an integer")

        if self.id < 1:
            raise ValueError("ID must be a positive integer (>0)")

    def mark_complete(self) -> None:
        """Mark this todo as complete."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark this todo as incomplete."""
        self.completed = False

    def update_description(self, new_description: str) -> None:
        """
        Update the todo description.

        Args:
            new_description: New description text

        Raises:
            ValueError: If new description fails validation
        """
        # Temporarily store old description
        old_description = self.description

        # Try to update (will validate via setter)
        self.description = new_description

        try:
            self._validate_description()
        except (ValueError, TypeError):
            # Restore old description if validation fails
            self.description = old_description
            raise

    def __repr__(self) -> str:
        """String representation for debugging."""
        status = "✓" if self.completed else " "
        return f"Todo(id={self.id}, [{status}] {self.description})"

    def __str__(self) -> str:
        """Human-readable string representation."""
        status = "Complete" if self.completed else "Incomplete"
        return f"[{self.id}] {self.description} ({status})"
```

### Storage Interface (Protocol)

```python
from typing import Protocol, Optional

class TodoStorage(Protocol):
    """Protocol defining storage interface for todos."""

    def save(self, todo: Todo) -> Todo:
        """
        Save a new todo.

        Args:
            todo: Todo to save (ID will be assigned)

        Returns:
            Saved todo with assigned ID
        """
        ...

    def find_by_id(self, id: int) -> Optional[Todo]:
        """
        Find todo by ID.

        Args:
            id: Todo ID to search for

        Returns:
            Todo if found, None otherwise
        """
        ...

    def find_all(self) -> list[Todo]:
        """
        Retrieve all todos.

        Returns:
            List of all todos
        """
        ...

    def find_by_status(self, completed: bool) -> list[Todo]:
        """
        Find todos by completion status.

        Args:
            completed: True for completed, False for incomplete

        Returns:
            List of todos matching status
        """
        ...

    def update(self, todo: Todo) -> None:
        """
        Update existing todo.

        Args:
            todo: Todo with updated values

        Raises:
            ValueError: If todo with given ID not found
        """
        ...

    def delete(self, id: int) -> None:
        """
        Delete todo by ID.

        Args:
            id: ID of todo to delete

        Note:
            Does not raise error if ID not found (idempotent)
        """
        ...

    def count(self) -> int:
        """
        Count total number of todos.

        Returns:
            Total todo count
        """
        ...
```

## Example Data

### Valid Todos

```python
# Minimal valid todo
Todo(id=1, description="Buy milk", completed=False)

# Complete todo
Todo(id=2, description="Finish homework", completed=True)

# Todo with long description
Todo(
    id=3,
    description="Research Python clean architecture patterns and implement a sample application demonstrating domain-driven design with proper separation of concerns",
    completed=False
)

# Todo with special characters
Todo(id=4, description="Read 'Clean Code' by Robert C. Martin", completed=False)

# Todo with emoji (UTF-8)
Todo(id=5, description="🎉 Celebrate project completion", completed=False)
```

### Invalid Todos (Validation Errors)

```python
# Empty description
Todo(id=1, description="", completed=False)
# Raises: ValueError("Description cannot be empty or whitespace-only")

# Whitespace-only description
Todo(id=1, description="   ", completed=False)
# Raises: ValueError("Description cannot be empty or whitespace-only")

# Description too long (>500 chars)
Todo(id=1, description="A" * 501, completed=False)
# Raises: ValueError("Description cannot exceed 500 characters")

# Invalid ID (zero)
Todo(id=0, description="Buy milk", completed=False)
# Raises: ValueError("ID must be a positive integer (>0)")

# Invalid ID (negative)
Todo(id=-1, description="Buy milk", completed=False)
# Raises: ValueError("ID must be a positive integer (>0)")

# Invalid type for description
Todo(id=1, description=123, completed=False)
# Raises: TypeError("Description must be a string")
```

## Relationships

**Phase I**: No relationships (single entity system)

**Future Phases**:
- Phase II: User → Todo (one-to-many) - when authentication added
- Phase III: Same structure, accessible via AI conversational interface
- Phase IV+: Same structure, persisted in database

## Migration Strategy

**Phase I → Phase II Migration**:
- Add `user_id` field to Todo entity (nullable initially for backward compatibility)
- Add `created_at` timestamp
- Add `updated_at` timestamp
- Keep all existing fields (id, description, completed)
- In-memory storage replaced with database (PostgreSQL via SQLModel)

**Backward Compatibility**:
- Core fields (id, description, completed) MUST remain unchanged
- New fields MUST be optional or have sensible defaults
- Validation rules MUST NOT become more restrictive

## Testing Checklist

**Entity Validation Tests**:
- ✅ Valid todo creation
- ✅ Empty description rejection
- ✅ Whitespace-only description rejection
- ✅ Description trimming
- ✅ Max length enforcement (500 chars)
- ✅ Invalid ID rejection (zero, negative)
- ✅ Type validation (non-string description, non-int ID)
- ✅ UTF-8 support (emoji, special characters)

**State Transition Tests**:
- ✅ New todo starts incomplete
- ✅ Mark complete transitions correctly
- ✅ Mark incomplete transitions correctly
- ✅ Multiple status toggles work correctly

**Business Rule Tests**:
- ✅ Auto-assigned ID is sequential
- ✅ ID is immutable after creation
- ✅ Description can be updated
- ✅ Updated description is validated

## Notes

- Data model is intentionally simple for Phase I (learning focus)
- All validation happens at entity level (fail fast)
- Storage interface defined as Protocol (enables easy testing with mocks)
- Future phases will extend this model without breaking changes
