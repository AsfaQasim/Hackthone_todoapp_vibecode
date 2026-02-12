"""
Todo domain entity with validation.

This module defines the core Todo entity following clean architecture principles.
The entity is framework-agnostic and contains only business logic and validation rules.
"""

from dataclasses import dataclass
from typing import ClassVar


@dataclass
class Todo:
    """
    Domain entity representing a todo item.

    Attributes:
        id: Unique identifier (auto-assigned by storage)
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
        self._validate_id()
        self._validate_description()

    def _validate_id(self) -> None:
        """Validate ID field."""
        if not isinstance(self.id, int):
            raise TypeError("ID must be an integer")

        if self.id < 0:
            raise ValueError("ID must be non-negative (0 for unassigned, ≥1 for assigned)")

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
            TypeError: If new description is not a string
        """
        # Temporarily store old description
        old_description = self.description

        # Try to update (will validate)
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
