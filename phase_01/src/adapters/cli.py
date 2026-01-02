"""
CLI adapter for the Todo application.

This module handles all user interaction via command-line interface.
It depends on the service layer and provides a menu-driven interface.
"""

import logging
from typing import Optional
from src.services.todo_service import TodoService
from src.domain.todo import Todo


class CLIAdapter:
    """
    CLI adapter providing menu-driven interface for todo management.

    Handles user input/output and translates to service operations.
    """

    def __init__(
        self, service: TodoService, logger: Optional[logging.Logger] = None
    ):
        """
        Initialize CLI adapter.

        Args:
            service: TodoService instance (injected)
            logger: Logger instance (injected, optional)
        """
        self._service = service
        self._logger = logger or logging.getLogger("todo-cli")
        self._running = True

    def run(self) -> None:
        """Run the main CLI loop."""
        self._display_welcome()

        while self._running:
            self._display_main_menu()
            choice = self._get_menu_choice(1, 8)

            if choice == 1:
                self._add_todo()
            elif choice == 2:
                self._view_all_todos()
            elif choice == 3:
                self._filter_todos()
            elif choice == 4:
                self._mark_complete()
            elif choice == 5:
                self._mark_incomplete()
            elif choice == 6:
                self._update_todo()
            elif choice == 7:
                self._delete_todo()
            elif choice == 8:
                self._exit()

    def _display_welcome(self) -> None:
        """Display welcome message."""
        print("\n" + "=" * 50)
        print("Welcome to Todo CLI!")
        print("=" * 50)

    def _display_main_menu(self) -> None:
        """Display main menu."""
        print("\n=== Todo CLI ===")
        print("1. Add Todo")
        print("2. View All Todos")
        print("3. Filter Todos")
        print("4. Mark Todo Complete")
        print("5. Mark Todo Incomplete")
        print("6. Update Todo")
        print("7. Delete Todo")
        print("8. Exit")

    def _display_filter_menu(self) -> None:
        """Display filter submenu."""
        print("\n=== Filter Todos ===")
        print("1. Show All")
        print("2. Show Complete Only")
        print("3. Show Incomplete Only")
        print("4. Back to Main Menu")

    def _get_menu_choice(self, min_choice: int, max_choice: int) -> int:
        """
        Get and validate menu choice.

        Args:
            min_choice: Minimum valid choice
            max_choice: Maximum valid choice

        Returns:
            Valid menu choice
        """
        while True:
            try:
                choice_str = input(
                    f"\nEnter your choice ({min_choice}-{max_choice}): "
                ).strip()
                choice = int(choice_str)

                if min_choice <= choice <= max_choice:
                    return choice
                else:
                    print(
                        f"✗ Error: Please enter a number between {min_choice}-{max_choice}."
                    )
            except ValueError:
                print("✗ Error: Please enter a valid number.")
            except (EOFError, KeyboardInterrupt):
                print("\n\nℹ️  Operation cancelled. Returning to main menu.")
                return max_choice  # Return back/exit option

    def _get_todo_id(self) -> Optional[int]:
        """
        Get and validate todo ID from user.

        Returns:
            Valid todo ID or None if user cancelled
        """
        while True:
            try:
                id_str = input("\nEnter todo ID: ").strip()
                if not id_str:
                    print("✗ Error: ID cannot be empty.")
                    continue

                todo_id = int(id_str)
                if todo_id < 1:
                    print("✗ Error: ID must be a positive number.")
                    continue

                return todo_id
            except ValueError:
                print("✗ Error: Please enter a valid number.")
            except (EOFError, KeyboardInterrupt):
                print("\n\nℹ️  Operation cancelled.")
                return None

    def _get_description(self, prompt: str = "Enter todo description: ") -> Optional[str]:
        """
        Get and validate todo description from user.

        Args:
            prompt: Prompt to display

        Returns:
            Valid description or None if user cancelled
        """
        try:
            description = input(f"\n{prompt}").strip()
            if not description:
                print("✗ Error: Description cannot be empty.")
                return None
            return description
        except (EOFError, KeyboardInterrupt):
            print("\n\nℹ️  Operation cancelled.")
            return None

    def _get_confirmation(self, prompt: str) -> bool:
        """
        Get yes/no confirmation from user.

        Args:
            prompt: Confirmation prompt

        Returns:
            True if confirmed, False otherwise
        """
        while True:
            try:
                response = input(f"\n{prompt} (y/n): ").strip().lower()
                if response in ["y", "yes"]:
                    return True
                elif response in ["n", "no"]:
                    return False
                else:
                    print("✗ Error: Please enter 'y' or 'n'.")
            except (EOFError, KeyboardInterrupt):
                print("\n\nℹ️  Operation cancelled.")
                return False

    def _add_todo(self) -> None:
        """Add a new todo."""
        description = self._get_description()
        if not description:
            return

        try:
            todo = self._service.create_todo(description)
            print(f"\n✓ Todo added successfully!")
            print(f"  ID: {todo.id}")
            print(f"  Description: {todo.description}")
            print(f"  Status: Incomplete")
            self._logger.info(f"User added todo: {todo.description}")
        except (ValueError, TypeError) as e:
            print(f"\n✗ Error: {e}")
            self._logger.error(f"Failed to add todo: {e}")

    def _view_all_todos(self) -> None:
        """View all todos."""
        todos = self._service.get_all_todos()

        print("\n=== All Todos ===\n")

        if not todos:
            print("No todos found. Use option 1 to add your first todo!")
            return

        self._display_todo_table(todos)

    def _display_todo_table(self, todos: list[Todo]) -> None:
        """
        Display todos in table format.

        Args:
            todos: List of todos to display
        """
        # Print header
        print(f"{'ID':<4} | {'Status':<12} | {'Description':<40}")
        print("-" * 4 + "-+-" + "-" * 12 + "-+-" + "-" * 40)

        # Print todos
        for todo in todos:
            status = "Complete" if todo.completed else "Incomplete"
            # Truncate long descriptions
            description = todo.description
            if len(description) > 40:
                description = description[:37] + "..."

            print(f"{todo.id:<4} | {status:<12} | {description:<40}")

        # Print summary
        completed_count = sum(1 for t in todos if t.completed)
        incomplete_count = len(todos) - completed_count
        print(
            f"\nTotal: {len(todos)} todo{'s' if len(todos) != 1 else ''} "
            f"({completed_count} complete, {incomplete_count} incomplete)"
        )

    def _filter_todos(self) -> None:
        """Filter todos by status."""
        while True:
            self._display_filter_menu()
            choice = self._get_menu_choice(1, 4)

            if choice == 1:
                self._view_all_todos()
                break
            elif choice == 2:
                self._view_completed_todos()
                break
            elif choice == 3:
                self._view_incomplete_todos()
                break
            elif choice == 4:
                break  # Back to main menu

    def _view_completed_todos(self) -> None:
        """View completed todos."""
        todos = self._service.get_completed_todos()

        print("\n=== Completed Todos ===\n")

        if not todos:
            print("No completed todos found.")
            return

        self._display_todo_table(todos)
# incomplete
    def _view_incomplete_todos(self) -> None:
        """View incomplete todos."""
        todos = self._service.get_incomplete_todos()

        print("\n=== Incomplete Todos ===\n")

        if not todos:
            print("No incomplete todos found.")
            return

        self._display_todo_table(todos)

    def _mark_complete(self) -> None:
        """Mark a todo as complete."""
        todo_id = self._get_todo_id()
        if todo_id is None:
            return

        todo = self._service.mark_complete(todo_id)

        if todo is None:
            print(
                f"\n✗ Error: Todo with ID {todo_id} not found. "
                "Use 'View All Todos' to see valid IDs."
            )
            return

        if todo.completed:
            # Check if it was already complete (log message from service)
            print(f"\n✓ Todo marked as complete!")
        else:
            print(f"\nℹ️  Todo was already complete.")

        print(f"  ID: {todo.id}")
        print(f"  Description: {todo.description}")
        print(f"  Status: Complete")

    def _mark_incomplete(self) -> None:
        """Mark a todo as incomplete."""
        todo_id = self._get_todo_id()
        if todo_id is None:
            return

        todo = self._service.mark_incomplete(todo_id)

        if todo is None:
            print(
                f"\n✗ Error: Todo with ID {todo_id} not found. "
                "Use 'View All Todos' to see valid IDs."
            )
            return

        if not todo.completed:
            print(f"\n✓ Todo marked as incomplete!")
        else:
            print(f"\nℹ️  Todo was already incomplete.")

        print(f"  ID: {todo.id}")
        print(f"  Description: {todo.description}")
        print(f"  Status: Incomplete")

    def _update_todo(self) -> None:
        """Update a todo's description."""
        todo_id = self._get_todo_id()
        if todo_id is None:
            return

        # Check if todo exists
        existing = self._service.get_todo_by_id(todo_id)
        if existing is None:
            print(
                f"\n✗ Error: Todo with ID {todo_id} not found. "
                "Use 'View All Todos' to see valid IDs."
            )
            return

        print(f"\nCurrent description: {existing.description}")

        new_description = self._get_description("Enter new description: ")
        if not new_description:
            return

        try:
            updated = self._service.update_todo(todo_id, new_description)

            if updated:
                print(f"\n✓ Todo updated successfully!")
                print(f"  ID: {updated.id}")
                print(f"  Old Description: {existing.description}")
                print(f"  New Description: {updated.description}")
                print(f"  Status: {'Complete' if updated.completed else 'Incomplete'}")
        except (ValueError, TypeError) as e:
            print(f"\n✗ Error: {e}")
# delete
    def _delete_todo(self) -> None:
        """Delete a todo."""
        todo_id = self._get_todo_id()
        if todo_id is None:
            return

        # Check if todo exists and get details for confirmation
        existing = self._service.get_todo_by_id(todo_id)
        if existing is None:
            print(
                f"\n✗ Error: Todo with ID {todo_id} not found. "
                "Use 'View All Todos' to see valid IDs."
            )
            return

        print(f"\nTodo to delete:")
        print(f"  ID: {existing.id}")
        print(f"  Description: {existing.description}")
        print(f"  Status: {'Complete' if existing.completed else 'Incomplete'}")

        confirmed = self._get_confirmation("Are you sure you want to delete this todo?")

        if not confirmed:
            print("\nℹ️  Deletion cancelled.")
            return

        success = self._service.delete_todo(todo_id)

        if success:
            print(f"\n✓ Todo deleted successfully!")
            print(f"  ID: {existing.id}")
            print(f"  Description: {existing.description}")

    def _exit(self) -> None:
        """Exit the application."""
        print("\nThank you for using Todo CLI! Goodbye.")
        self._running = False
