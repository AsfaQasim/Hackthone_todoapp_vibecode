"""
Integration tests for CLI workflows.

Tests end-to-end user scenarios with all layers integrated.
"""

import pytest
from src.infrastructure.storage import InMemoryStorage
from src.infrastructure.logger import setup_logger
from src.services.todo_service import TodoService


@pytest.fixture
def service() -> TodoService:
    """Provide integrated service with all dependencies."""
    storage = InMemoryStorage()
    logger = setup_logger(name="test-cli", log_file="test-cli.log")
    return TodoService(storage=storage, logger=logger)


class TestAddTodoWorkflow:
    """Test add todo workflow."""

    def test_add_and_retrieve_todo(self, service: TodoService) -> None:
        """Test adding a todo and retrieving it."""
        # Add todo
        todo = service.create_todo("Buy groceries")

        # Verify created
        assert todo.id == 1
        assert todo.description == "Buy groceries"
        assert todo.completed is False

        # Retrieve todo
        found = service.get_todo_by_id(todo.id)
        assert found is not None
        assert found.description == "Buy groceries"

    def test_add_multiple_todos(self, service: TodoService) -> None:
        """Test adding multiple todos."""
        todo1 = service.create_todo("Buy groceries")
        todo2 = service.create_todo("Finish homework")
        todo3 = service.create_todo("Call mom")

        todos = service.get_all_todos()

        assert len(todos) == 3
        assert todos[0].id == 1
        assert todos[1].id == 2
        assert todos[2].id == 3


class TestViewTodosWorkflow:
    """Test view todos workflow."""

    def test_view_empty_list(self, service: TodoService) -> None:
        """Test viewing empty todo list."""
        todos = service.get_all_todos()

        assert len(todos) == 0

    def test_view_all_todos(self, service: TodoService) -> None:
        """Test viewing all todos."""
        service.create_todo("Todo 1")
        service.create_todo("Todo 2")
        service.create_todo("Todo 3")

        todos = service.get_all_todos()

        assert len(todos) == 3


class TestMarkCompleteWorkflow:
    """Test mark complete workflow."""

    def test_mark_todo_complete(self, service: TodoService) -> None:
        """Test marking todo complete."""
        todo = service.create_todo("Buy groceries")

        updated = service.mark_complete(todo.id)

        assert updated is not None
        assert updated.completed is True


class TestMarkIncompleteWorkflow:
    """Test mark incomplete workflow."""

    def test_mark_todo_incomplete(self, service: TodoService) -> None:
        """Test marking todo incomplete."""
        todo = service.create_todo("Buy groceries")
        service.mark_complete(todo.id)

        updated = service.mark_incomplete(todo.id)

        assert updated is not None
        assert updated.completed is False


class TestFilterWorkflow:
    """Test filter todos workflow."""

    def test_filter_by_complete(self, service: TodoService) -> None:
        """Test filtering completed todos."""
        todo1 = service.create_todo("Todo 1")
        service.create_todo("Todo 2")
        todo3 = service.create_todo("Todo 3")

        service.mark_complete(todo1.id)
        service.mark_complete(todo3.id)

        completed = service.get_completed_todos()

        assert len(completed) == 2
        assert all(t.completed for t in completed)

    def test_filter_by_incomplete(self, service: TodoService) -> None:
        """Test filtering incomplete todos."""
        service.create_todo("Todo 1")
        todo2 = service.create_todo("Todo 2")
        service.create_todo("Todo 3")

        service.mark_complete(todo2.id)

        incomplete = service.get_incomplete_todos()

        assert len(incomplete) == 2
        assert all(not t.completed for t in incomplete)


class TestUpdateWorkflow:
    """Test update todo workflow."""

    def test_update_todo_description(self, service: TodoService) -> None:
        """Test updating todo description."""
        todo = service.create_todo("Buy groseries")

        updated = service.update_todo(todo.id, "Buy groceries")

        assert updated is not None
        assert updated.description == "Buy groceries"


class TestDeleteWorkflow:
    """Test delete todo workflow."""

    def test_delete_todo(self, service: TodoService) -> None:
        """Test deleting todo."""
        todo = service.create_todo("Buy groceries")

        success = service.delete_todo(todo.id)

        assert success is True
        assert service.get_todo_by_id(todo.id) is None


class TestFullWorkflow:
    """Test complete user workflow."""

    def test_complete_user_journey(self, service: TodoService) -> None:
        """Test full user journey: add, view, mark, filter, update, delete."""
        # Add 3 todos
        todo1 = service.create_todo("Buy groceries")
        todo2 = service.create_todo("Finish homework")
        todo3 = service.create_todo("Call mom")

        # Mark 1 complete
        service.mark_complete(todo1.id)

        # Filter by status
        completed = service.get_completed_todos()
        incomplete = service.get_incomplete_todos()

        assert len(completed) == 1
        assert len(incomplete) == 2

        # Update 1
        service.update_todo(todo2.id, "Finish math homework")

        # Delete 1
        service.delete_todo(todo3.id)

        # Verify final state
        final_todos = service.get_all_todos()
        assert len(final_todos) == 2
        assert final_todos[0].completed is True
        assert final_todos[1].description == "Finish math homework"
