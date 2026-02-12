"""
Unit tests for Todo domain entity.

Tests entity validation, state transitions, and business rules.
"""

import pytest
from src.domain.todo import Todo


class TestTodoCreation:
    """Test todo creation and validation."""

    def test_create_valid_todo(self) -> None:
        """Test creating a valid todo."""
        todo = Todo(id=1, description="Buy groceries", completed=False)
        assert todo.id == 1
        assert todo.description == "Buy groceries"
        assert todo.completed is False

    def test_create_todo_with_whitespace(self) -> None:
        """Test that whitespace is trimmed from description."""
        todo = Todo(id=1, description="  Buy groceries  ", completed=False)
        assert todo.description == "Buy groceries"

    def test_create_todo_default_incomplete(self) -> None:
        """Test that todos default to incomplete status."""
        todo = Todo(id=1, description="Buy groceries")
        assert todo.completed is False

    def test_empty_description_rejected(self) -> None:
        """Test that empty description is rejected."""
        with pytest.raises(ValueError, match="cannot be empty"):
            Todo(id=1, description="", completed=False)

    def test_whitespace_only_description_rejected(self) -> None:
        """Test that whitespace-only description is rejected."""
        with pytest.raises(ValueError, match="cannot be empty"):
            Todo(id=1, description="   ", completed=False)

    def test_long_description_rejected(self) -> None:
        """Test that description exceeding 500 chars is rejected."""
        long_description = "A" * 501
        with pytest.raises(ValueError, match="cannot exceed 500 characters"):
            Todo(id=1, description=long_description, completed=False)

    def test_max_length_description_accepted(self) -> None:
        """Test that 500 character description is accepted."""
        max_description = "A" * 500
        todo = Todo(id=1, description=max_description, completed=False)
        assert len(todo.description) == 500

    def test_zero_id_accepted(self) -> None:
        """Test that ID of zero is accepted (placeholder for unassigned)."""
        todo = Todo(id=0, description="Buy groceries", completed=False)
        assert todo.id == 0

    def test_negative_id_rejected(self) -> None:
        """Test that negative ID is rejected."""
        with pytest.raises(ValueError, match="must be non-negative"):
            Todo(id=-1, description="Buy groceries", completed=False)

    def test_non_string_description_rejected(self) -> None:
        """Test that non-string description is rejected."""
        with pytest.raises(TypeError, match="must be a string"):
            Todo(id=1, description=123, completed=False)  # type: ignore

    def test_non_int_id_rejected(self) -> None:
        """Test that non-integer ID is rejected."""
        with pytest.raises(TypeError, match="must be an integer"):
            Todo(id="1", description="Buy groceries", completed=False)  # type: ignore

    def test_utf8_description_supported(self) -> None:
        """Test that UTF-8 characters (emoji) are supported."""
        todo = Todo(id=1, description="🎉 Celebrate", completed=False)
        assert todo.description == "🎉 Celebrate"


class TestTodoStateTransitions:
    """Test todo state transitions."""

    def test_mark_complete(self) -> None:
        """Test marking todo as complete."""
        todo = Todo(id=1, description="Buy groceries", completed=False)
        todo.mark_complete()
        assert todo.completed is True

    def test_mark_incomplete(self) -> None:
        """Test marking todo as incomplete."""
        todo = Todo(id=1, description="Buy groceries", completed=True)
        todo.mark_incomplete()
        assert todo.completed is False

    def test_toggle_status_multiple_times(self) -> None:
        """Test toggling status multiple times."""
        todo = Todo(id=1, description="Buy groceries", completed=False)

        todo.mark_complete()
        assert todo.completed is True

        todo.mark_incomplete()
        assert todo.completed is False

        todo.mark_complete()
        assert todo.completed is True


class TestTodoUpdate:
    """Test todo update operations."""

    def test_update_description(self) -> None:
        """Test updating todo description."""
        todo = Todo(id=1, description="Buy groseries", completed=False)
        todo.update_description("Buy groceries")
        assert todo.description == "Buy groceries"

    def test_update_description_with_whitespace(self) -> None:
        """Test that whitespace is trimmed on update."""
        todo = Todo(id=1, description="Buy groceries", completed=False)
        todo.update_description("  Buy milk  ")
        assert todo.description == "Buy milk"

    def test_update_with_empty_description_rejected(self) -> None:
        """Test that updating to empty description is rejected and original is kept."""
        todo = Todo(id=1, description="Buy groceries", completed=False)
        with pytest.raises(ValueError, match="cannot be empty"):
            todo.update_description("")
        # Verify original description is preserved
        assert todo.description == "Buy groceries"

    def test_update_with_long_description_rejected(self) -> None:
        """Test that updating to too-long description is rejected and original is kept."""
        todo = Todo(id=1, description="Buy groceries", completed=False)
        long_description = "A" * 501
        with pytest.raises(ValueError, match="cannot exceed 500 characters"):
            todo.update_description(long_description)
        # Verify original description is preserved
        assert todo.description == "Buy groceries"


class TestTodoStringRepresentation:
    """Test todo string representations."""

    def test_str_incomplete(self) -> None:
        """Test string representation of incomplete todo."""
        todo = Todo(id=1, description="Buy groceries", completed=False)
        assert str(todo) == "[1] Buy groceries (Incomplete)"

    def test_str_complete(self) -> None:
        """Test string representation of complete todo."""
        todo = Todo(id=2, description="Finish homework", completed=True)
        assert str(todo) == "[2] Finish homework (Complete)"

    def test_repr_incomplete(self) -> None:
        """Test repr of incomplete todo."""
        todo = Todo(id=1, description="Buy groceries", completed=False)
        repr_str = repr(todo)
        assert "Todo(id=1" in repr_str
        assert "Buy groceries" in repr_str
        assert "[ ]" in repr_str

    def test_repr_complete(self) -> None:
        """Test repr of complete todo."""
        todo = Todo(id=1, description="Buy groceries", completed=True)
        repr_str = repr(todo)
        assert "Todo(id=1" in repr_str
        assert "Buy groceries" in repr_str
        assert "[✓]" in repr_str
