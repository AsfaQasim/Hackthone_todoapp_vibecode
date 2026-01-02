"""
Unit tests for InMemoryStorage.

Tests storage CRUD operations, ID generation, and data integrity.
"""

import pytest
from src.domain.todo import Todo
from src.infrastructure.storage import InMemoryStorage


class TestStorageSave:
    """Test saving todos to storage."""

    def test_save_todo_assigns_id(self) -> None:
        """Test that saving assigns sequential ID."""
        storage = InMemoryStorage()
        todo = Todo(id=0, description="Buy groceries", completed=False)

        saved = storage.save(todo)

        assert saved.id == 1
        assert saved.description == "Buy groceries"

    def test_save_multiple_todos_sequential_ids(self) -> None:
        """Test that multiple saves assign sequential IDs."""
        storage = InMemoryStorage()

        todo1 = storage.save(Todo(id=0, description="Todo 1", completed=False))
        todo2 = storage.save(Todo(id=0, description="Todo 2", completed=False))
        todo3 = storage.save(Todo(id=0, description="Todo 3", completed=False))

        assert todo1.id == 1
        assert todo2.id == 2
        assert todo3.id == 3


class TestStorageFindById:
    """Test finding todos by ID."""

    def test_find_by_id_existing(self) -> None:
        """Test finding existing todo by ID."""
        storage = InMemoryStorage()
        saved = storage.save(Todo(id=0, description="Buy groceries", completed=False))

        found = storage.find_by_id(saved.id)

        assert found is not None
        assert found.id == saved.id
        assert found.description == "Buy groceries"

    def test_find_by_id_non_existent(self) -> None:
        """Test finding non-existent todo returns None."""
        storage = InMemoryStorage()

        found = storage.find_by_id(999)

        assert found is None

    def test_find_by_id_after_multiple_saves(self) -> None:
        """Test finding specific todo after saving multiple."""
        storage = InMemoryStorage()
        todo1 = storage.save(Todo(id=0, description="Todo 1", completed=False))
        todo2 = storage.save(Todo(id=0, description="Todo 2", completed=False))
        todo3 = storage.save(Todo(id=0, description="Todo 3", completed=False))

        found = storage.find_by_id(todo2.id)

        assert found is not None
        assert found.id == todo2.id
        assert found.description == "Todo 2"


class TestStorageFindAll:
    """Test finding all todos."""

    def test_find_all_empty(self) -> None:
        """Test finding all todos when storage is empty."""
        storage = InMemoryStorage()

        todos = storage.find_all()

        assert len(todos) == 0

    def test_find_all_multiple_todos(self) -> None:
        """Test finding all todos returns all saved todos."""
        storage = InMemoryStorage()
        storage.save(Todo(id=0, description="Todo 1", completed=False))
        storage.save(Todo(id=0, description="Todo 2", completed=True))
        storage.save(Todo(id=0, description="Todo 3", completed=False))

        todos = storage.find_all()

        assert len(todos) == 3
        assert todos[0].description == "Todo 1"
        assert todos[1].description == "Todo 2"
        assert todos[2].description == "Todo 3"

    def test_find_all_returns_copy(self) -> None:
        """Test that find_all returns a copy to prevent external mutation."""
        storage = InMemoryStorage()
        storage.save(Todo(id=0, description="Todo 1", completed=False))

        todos1 = storage.find_all()
        todos2 = storage.find_all()

        # Modifying returned list should not affect storage
        todos1.clear()

        assert len(todos2) == 1
        assert len(storage.find_all()) == 1


class TestStorageFindByStatus:
    """Test finding todos by completion status."""

    def test_find_by_status_completed(self) -> None:
        """Test finding completed todos."""
        storage = InMemoryStorage()
        storage.save(Todo(id=0, description="Todo 1", completed=False))
        storage.save(Todo(id=0, description="Todo 2", completed=True))
        storage.save(Todo(id=0, description="Todo 3", completed=True))

        completed = storage.find_by_status(completed=True)

        assert len(completed) == 2
        assert completed[0].description == "Todo 2"
        assert completed[1].description == "Todo 3"

    def test_find_by_status_incomplete(self) -> None:
        """Test finding incomplete todos."""
        storage = InMemoryStorage()
        storage.save(Todo(id=0, description="Todo 1", completed=False))
        storage.save(Todo(id=0, description="Todo 2", completed=True))
        storage.save(Todo(id=0, description="Todo 3", completed=False))

        incomplete = storage.find_by_status(completed=False)

        assert len(incomplete) == 2
        assert incomplete[0].description == "Todo 1"
        assert incomplete[1].description == "Todo 3"

    def test_find_by_status_none_matching(self) -> None:
        """Test finding todos when none match status."""
        storage = InMemoryStorage()
        storage.save(Todo(id=0, description="Todo 1", completed=False))

        completed = storage.find_by_status(completed=True)

        assert len(completed) == 0


class TestStorageUpdate:
    """Test updating todos."""

    def test_update_existing_todo(self) -> None:
        """Test updating existing todo."""
        storage = InMemoryStorage()
        saved = storage.save(Todo(id=0, description="Buy groceries", completed=False))

        saved.description = "Buy milk"
        saved.completed = True
        storage.update(saved)

        updated = storage.find_by_id(saved.id)
        assert updated is not None
        assert updated.description == "Buy milk"
        assert updated.completed is True

    def test_update_non_existent_todo_raises_error(self) -> None:
        """Test that updating non-existent todo raises error."""
        storage = InMemoryStorage()
        non_existent = Todo(id=999, description="Does not exist", completed=False)

        with pytest.raises(ValueError, match="not found"):
            storage.update(non_existent)


class TestStorageDelete:
    """Test deleting todos."""

    def test_delete_existing_todo(self) -> None:
        """Test deleting existing todo."""
        storage = InMemoryStorage()
        saved = storage.save(Todo(id=0, description="Buy groceries", completed=False))

        storage.delete(saved.id)

        assert storage.find_by_id(saved.id) is None
        assert len(storage.find_all()) == 0

    def test_delete_non_existent_todo_idempotent(self) -> None:
        """Test that deleting non-existent todo does not raise error."""
        storage = InMemoryStorage()

        # Should not raise error
        storage.delete(999)

        assert len(storage.find_all()) == 0

    def test_delete_does_not_reuse_id(self) -> None:
        """Test that deleted IDs are not reused."""
        storage = InMemoryStorage()
        todo1 = storage.save(Todo(id=0, description="Todo 1", completed=False))
        storage.delete(todo1.id)

        todo2 = storage.save(Todo(id=0, description="Todo 2", completed=False))

        # ID should be 2, not 1
        assert todo2.id == 2


class TestStorageCount:
    """Test counting todos."""

    def test_count_empty_storage(self) -> None:
        """Test count on empty storage."""
        storage = InMemoryStorage()

        assert storage.count() == 0

    def test_count_after_saves(self) -> None:
        """Test count after saving todos."""
        storage = InMemoryStorage()
        storage.save(Todo(id=0, description="Todo 1", completed=False))
        storage.save(Todo(id=0, description="Todo 2", completed=False))
        storage.save(Todo(id=0, description="Todo 3", completed=False))

        assert storage.count() == 3

    def test_count_after_delete(self) -> None:
        """Test count after deleting todo."""
        storage = InMemoryStorage()
        todo1 = storage.save(Todo(id=0, description="Todo 1", completed=False))
        storage.save(Todo(id=0, description="Todo 2", completed=False))

        storage.delete(todo1.id)

        assert storage.count() == 1
