"""
Unit tests for TodoService.

Tests business logic, service operations, and integration with storage.
"""

import pytest
import logging
from src.domain.todo import Todo
from src.services.todo_service import TodoService
from src.infrastructure.storage import InMemoryStorage


@pytest.fixture
def storage() -> InMemoryStorage:
    """Provide fresh storage for each test."""
    return InMemoryStorage()


@pytest.fixture
def logger() -> logging.Logger:
    """Provide logger for tests."""
    logger = logging.getLogger("test-logger")
    logger.setLevel(logging.DEBUG)
    return logger


@pytest.fixture
def service(storage: InMemoryStorage, logger: logging.Logger) -> TodoService:
    """Provide TodoService with dependencies."""
    return TodoService(storage=storage, logger=logger)


class TestServiceCreateTodo:
    """Test creating todos via service."""

    def test_create_todo(self, service: TodoService) -> None:
        """Test creating a todo."""
        todo = service.create_todo("Buy groceries")

        assert todo.id == 1
        assert todo.description == "Buy groceries"
        assert todo.completed is False

    def test_create_todo_trimmed(self, service: TodoService) -> None:
        """Test that description is trimmed."""
        todo = service.create_todo("  Buy groceries  ")

        assert todo.description == "Buy groceries"

    def test_create_todo_empty_description_raises_error(
        self, service: TodoService
    ) -> None:
        """Test that empty description raises error."""
        with pytest.raises(ValueError, match="cannot be empty"):
            service.create_todo("")

    def test_create_multiple_todos(self, service: TodoService) -> None:
        """Test creating multiple todos assigns sequential IDs."""
        todo1 = service.create_todo("Todo 1")
        todo2 = service.create_todo("Todo 2")
        todo3 = service.create_todo("Todo 3")

        assert todo1.id == 1
        assert todo2.id == 2
        assert todo3.id == 3


class TestServiceGetTodo:
    """Test retrieving todos."""

    def test_get_todo_by_id(self, service: TodoService) -> None:
        """Test getting todo by ID."""
        created = service.create_todo("Buy groceries")

        found = service.get_todo_by_id(created.id)

        assert found is not None
        assert found.id == created.id
        assert found.description == "Buy groceries"

    def test_get_todo_by_id_non_existent(self, service: TodoService) -> None:
        """Test getting non-existent todo returns None."""
        found = service.get_todo_by_id(999)

        assert found is None

    def test_get_all_todos_empty(self, service: TodoService) -> None:
        """Test getting all todos when none exist."""
        todos = service.get_all_todos()

        assert len(todos) == 0

    def test_get_all_todos(self, service: TodoService) -> None:
        """Test getting all todos."""
        service.create_todo("Todo 1")
        service.create_todo("Todo 2")
        service.create_todo("Todo 3")

        todos = service.get_all_todos()

        assert len(todos) == 3

    def test_get_completed_todos(self, service: TodoService) -> None:
        """Test getting completed todos."""
        todo1 = service.create_todo("Todo 1")
        service.create_todo("Todo 2")
        todo3 = service.create_todo("Todo 3")

        service.mark_complete(todo1.id)
        service.mark_complete(todo3.id)

        completed = service.get_completed_todos()

        assert len(completed) == 2
        assert completed[0].id == todo1.id
        assert completed[1].id == todo3.id

    def test_get_incomplete_todos(self, service: TodoService) -> None:
        """Test getting incomplete todos."""
        todo1 = service.create_todo("Todo 1")
        todo2 = service.create_todo("Todo 2")
        todo3 = service.create_todo("Todo 3")

        service.mark_complete(todo2.id)

        incomplete = service.get_incomplete_todos()

        assert len(incomplete) == 2
        assert incomplete[0].id == todo1.id
        assert incomplete[1].id == todo3.id


class TestServiceMarkComplete:
    """Test marking todos complete."""

    def test_mark_complete(self, service: TodoService) -> None:
        """Test marking todo complete."""
        todo = service.create_todo("Buy groceries")

        updated = service.mark_complete(todo.id)

        assert updated is not None
        assert updated.completed is True

        # Verify via get
        found = service.get_todo_by_id(todo.id)
        assert found is not None
        assert found.completed is True

    def test_mark_complete_non_existent(self, service: TodoService) -> None:
        """Test marking non-existent todo returns None."""
        updated = service.mark_complete(999)

        assert updated is None

    def test_mark_complete_already_complete(self, service: TodoService) -> None:
        """Test marking already complete todo."""
        todo = service.create_todo("Buy groceries")
        service.mark_complete(todo.id)

        # Mark complete again
        updated = service.mark_complete(todo.id)

        assert updated is not None
        assert updated.completed is True


class TestServiceMarkIncomplete:
    """Test marking todos incomplete."""

    def test_mark_incomplete(self, service: TodoService) -> None:
        """Test marking todo incomplete."""
        todo = service.create_todo("Buy groceries")
        service.mark_complete(todo.id)

        updated = service.mark_incomplete(todo.id)

        assert updated is not None
        assert updated.completed is False

    def test_mark_incomplete_non_existent(self, service: TodoService) -> None:
        """Test marking non-existent todo returns None."""
        updated = service.mark_incomplete(999)

        assert updated is None

    def test_mark_incomplete_already_incomplete(
        self, service: TodoService
    ) -> None:
        """Test marking already incomplete todo."""
        todo = service.create_todo("Buy groceries")

        # Mark incomplete (already incomplete)
        updated = service.mark_incomplete(todo.id)

        assert updated is not None
        assert updated.completed is False


class TestServiceUpdateTodo:
    """Test updating todos."""

    def test_update_todo(self, service: TodoService) -> None:
        """Test updating todo description."""
        todo = service.create_todo("Buy groseries")

        updated = service.update_todo(todo.id, "Buy groceries")

        assert updated is not None
        assert updated.description == "Buy groceries"

        # Verify via get
        found = service.get_todo_by_id(todo.id)
        assert found is not None
        assert found.description == "Buy groceries"

    def test_update_todo_non_existent(self, service: TodoService) -> None:
        """Test updating non-existent todo returns None."""
        updated = service.update_todo(999, "New description")

        assert updated is None

    def test_update_todo_empty_description_raises_error(
        self, service: TodoService
    ) -> None:
        """Test that updating to empty description raises error."""
        todo = service.create_todo("Buy groceries")

        with pytest.raises(ValueError, match="cannot be empty"):
            service.update_todo(todo.id, "")

        # Verify original description preserved
        found = service.get_todo_by_id(todo.id)
        assert found is not None
        assert found.description == "Buy groceries"


class TestServiceDeleteTodo:
    """Test deleting todos."""

    def test_delete_todo(self, service: TodoService) -> None:
        """Test deleting todo."""
        todo = service.create_todo("Buy groceries")

        result = service.delete_todo(todo.id)

        assert result is True
        assert service.get_todo_by_id(todo.id) is None

    def test_delete_todo_non_existent(self, service: TodoService) -> None:
        """Test deleting non-existent todo returns False."""
        result = service.delete_todo(999)

        assert result is False

    def test_delete_todo_removes_from_list(self, service: TodoService) -> None:
        """Test that deleted todo is removed from all todos list."""
        todo1 = service.create_todo("Todo 1")
        service.create_todo("Todo 2")

        service.delete_todo(todo1.id)

        todos = service.get_all_todos()
        assert len(todos) == 1
        assert todos[0].description == "Todo 2"


class TestServiceGetTodoCount:
    """Test counting todos."""

    def test_get_todo_count_empty(self, service: TodoService) -> None:
        """Test count when no todos exist."""
        count = service.get_todo_count()

        assert count == 0

    def test_get_todo_count(self, service: TodoService) -> None:
        """Test count after creating todos."""
        service.create_todo("Todo 1")
        service.create_todo("Todo 2")
        service.create_todo("Todo 3")

        count = service.get_todo_count()

        assert count == 3

    def test_get_todo_count_after_delete(self, service: TodoService) -> None:
        """Test count after deleting todo."""
        todo1 = service.create_todo("Todo 1")
        service.create_todo("Todo 2")

        service.delete_todo(todo1.id)

        count = service.get_todo_count()

        assert count == 1
