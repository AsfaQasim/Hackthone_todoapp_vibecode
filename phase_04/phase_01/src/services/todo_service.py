"""
Todo service layer containing business logic.

This module implements CRUD operations and business rules for todos.
It depends only on the domain layer and uses injected storage.
"""

from typing import Optional
import logging
from src.domain.todo import Todo
from src.infrastructure.storage import TodoStorage


class TodoService:
    """
    Service layer for todo business logic.

    Handles CRUD operations and enforces business rules.
    """

    def __init__(self, storage: TodoStorage, logger: Optional[logging.Logger] = None):
        """
        Initialize service with dependencies.

        Args:
            storage: Storage implementation (injected)
            logger: Logger instance (injected, optional)
        """
        self._storage = storage
        self._logger = logger or logging.getLogger("todo-cli")

    def create_todo(self, description: str) -> Todo:
        """
        Create a new todo.

        Args:
            description: Todo description

        Returns:
            Created todo with assigned ID

        Raises:
            ValueError: If description is invalid
            TypeError: If description is not a string
        """
        # Create todo (validation happens in Todo.__post_init__)
        todo = Todo(id=0, description=description, completed=False)

        # Save todo (storage assigns actual ID)
        saved_todo = self._storage.save(todo)

        self._logger.info(
            f"Created todo: {saved_todo.description}",
            extra={"todo_id": saved_todo.id, "operation": "create"}
        )

        return saved_todo

    def get_todo_by_id(self, id: int) -> Optional[Todo]:
        """
        Get todo by ID.

        Args:
            id: Todo ID

        Returns:
            Todo if found, None otherwise
        """
        todo = self._storage.find_by_id(id)

        if todo:
            self._logger.debug(
                f"Found todo: {todo.description}",
                extra={"todo_id": id, "operation": "get"}
            )
        else:
            self._logger.debug(
                f"Todo not found: {id}",
                extra={"todo_id": id, "operation": "get"}
            )

        return todo

    def get_all_todos(self) -> list[Todo]:
        """
        Get all todos.

        Returns:
            List of all todos
        """
        todos = self._storage.find_all()

        self._logger.debug(
            f"Retrieved all todos: {len(todos)} found",
            extra={"operation": "get_all", "count": len(todos)}
        )

        return todos

    def get_completed_todos(self) -> list[Todo]:
        """
        Get completed todos.

        Returns:
            List of completed todos
        """
        todos = self._storage.find_by_status(completed=True)

        self._logger.debug(
            f"Retrieved completed todos: {len(todos)} found",
            extra={"operation": "get_completed", "count": len(todos)}
        )

        return todos

    def get_incomplete_todos(self) -> list[Todo]:
        """
        Get incomplete todos.

        Returns:
            List of incomplete todos
        """
        todos = self._storage.find_by_status(completed=False)

        self._logger.debug(
            f"Retrieved incomplete todos: {len(todos)} found",
            extra={"operation": "get_incomplete", "count": len(todos)}
        )

        return todos

    def mark_complete(self, id: int) -> Optional[Todo]:
        """
        Mark todo as complete.

        Args:
            id: Todo ID

        Returns:
            Updated todo if found, None otherwise
        """
        todo = self._storage.find_by_id(id)

        if not todo:
            self._logger.warning(
                f"Cannot mark complete: todo not found",
                extra={"todo_id": id, "operation": "mark_complete"}
            )
            return None

        # Check if already complete
        if todo.completed:
            self._logger.info(
                f"Todo already complete: {todo.description}",
                extra={"todo_id": id, "operation": "mark_complete"}
            )
            return todo

        todo.mark_complete()
        self._storage.update(todo)

        self._logger.info(
            f"Marked todo complete: {todo.description}",
            extra={"todo_id": id, "operation": "mark_complete"}
        )

        return todo

    def mark_incomplete(self, id: int) -> Optional[Todo]:
        """
        Mark todo as incomplete.

        Args:
            id: Todo ID

        Returns:
            Updated todo if found, None otherwise
        """
        todo = self._storage.find_by_id(id)

        if not todo:
            self._logger.warning(
                f"Cannot mark incomplete: todo not found",
                extra={"todo_id": id, "operation": "mark_incomplete"}
            )
            return None

        # Check if already incomplete
        if not todo.completed:
            self._logger.info(
                f"Todo already incomplete: {todo.description}",
                extra={"todo_id": id, "operation": "mark_incomplete"}
            )
            return todo

        todo.mark_incomplete()
        self._storage.update(todo)

        self._logger.info(
            f"Marked todo incomplete: {todo.description}",
            extra={"todo_id": id, "operation": "mark_incomplete"}
        )

        return todo

    def update_todo(self, id: int, new_description: str) -> Optional[Todo]:
        """
        Update todo description.

        Args:
            id: Todo ID
            new_description: New description

        Returns:
            Updated todo if found, None otherwise

        Raises:
            ValueError: If new description is invalid
            TypeError: If new description is not a string
        """
        todo = self._storage.find_by_id(id)

        if not todo:
            self._logger.warning(
                f"Cannot update: todo not found",
                extra={"todo_id": id, "operation": "update"}
            )
            return None

        old_description = todo.description
        todo.update_description(new_description)
        self._storage.update(todo)

        self._logger.info(
            f"Updated todo: '{old_description}' → '{new_description}'",
            extra={"todo_id": id, "operation": "update"}
        )

        return todo

    def delete_todo(self, id: int) -> bool:
        """
        Delete todo.

        Args:
            id: Todo ID

        Returns:
            True if todo was found and deleted, False if not found
        """
        todo = self._storage.find_by_id(id)

        if not todo:
            self._logger.warning(
                f"Cannot delete: todo not found",
                extra={"todo_id": id, "operation": "delete"}
            )
            return False

        self._storage.delete(id)

        self._logger.info(
            f"Deleted todo: {todo.description}",
            extra={"todo_id": id, "operation": "delete"}
        )

        return True

    def get_todo_count(self) -> int:
        """
        Get total number of todos.

        Returns:
            Total todo count
        """
        count = self._storage.count()

        self._logger.debug(
            f"Total todos: {count}",
            extra={"operation": "count", "count": count}
        )

        return count
