"""
Storage infrastructure for todos.

This module defines the storage interface (protocol) and in-memory implementation.
Following clean architecture, the storage is injected into services.
"""

from typing import Protocol, Optional
from src.domain.todo import Todo


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


class InMemoryStorage:
    """
    In-memory implementation of TodoStorage.

    Stores todos in a Python list with sequential ID generation.
    """

    def __init__(self) -> None:
        """Initialize empty storage."""
        self._todos: list[Todo] = []
        self._next_id: int = 1

    def save(self, todo: Todo) -> Todo:
        """
        Save a new todo and assign ID.

        Args:
            todo: Todo to save (ID will be overwritten)

        Returns:
            Saved todo with assigned ID
        """
        todo.id = self._next_id
        self._next_id += 1
        self._todos.append(todo)
        return todo

    def find_by_id(self, id: int) -> Optional[Todo]:
        """
        Find todo by ID.

        Args:
            id: Todo ID to search for

        Returns:
            Todo if found, None otherwise
        """
        for todo in self._todos:
            if todo.id == id:
                return todo
        return None

    def find_all(self) -> list[Todo]:
        """
        Return all todos.

        Returns:
            Copy of todos list to prevent external mutation
        """
        return self._todos.copy()

    def find_by_status(self, completed: bool) -> list[Todo]:
        """
        Find todos by completion status.

        Args:
            completed: True for completed, False for incomplete

        Returns:
            List of todos matching status
        """
        return [todo for todo in self._todos if todo.completed == completed]

    def update(self, todo: Todo) -> None:
        """
        Update existing todo.

        Args:
            todo: Todo with updated values

        Raises:
            ValueError: If todo with given ID not found
        """
        for i, existing in enumerate(self._todos):
            if existing.id == todo.id:
                self._todos[i] = todo
                return
        raise ValueError(f"Todo with ID {todo.id} not found")

    def delete(self, id: int) -> None:
        """
        Delete todo by ID (idempotent).

        Args:
            id: ID of todo to delete
        """
        self._todos = [t for t in self._todos if t.id != id]

    def count(self) -> int:
        """
        Count total number of todos.

        Returns:
            Total todo count
        """
        return len(self._todos)
