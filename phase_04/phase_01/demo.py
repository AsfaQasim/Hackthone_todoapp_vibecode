"""
Demo script to showcase the Todo CLI application.

This script programmatically demonstrates all features without requiring user input.
"""

from src.infrastructure.storage import InMemoryStorage
from src.infrastructure.logger import setup_logger
from src.services.todo_service import TodoService


def print_separator():
    """Print a visual separator."""
    print("\n" + "=" * 70)


def print_todos_table(todos, title="Todos"):
    """Display todos in table format."""
    print(f"\n{title}:")
    print("-" * 70)

    if not todos:
        print("  No todos found.")
        return

    print(f"{'ID':<4} | {'Status':<12} | {'Description':<40}")
    print("-" * 4 + "-+-" + "-" * 12 + "-+-" + "-" * 40)

    for todo in todos:
        status = "Complete" if todo.completed else "Incomplete"
        description = todo.description
        if len(description) > 40:
            description = description[:37] + "..."
        print(f"{todo.id:<4} | {status:<12} | {description:<40}")

    completed_count = sum(1 for t in todos if t.completed)
    incomplete_count = len(todos) - completed_count
    print(f"\nTotal: {len(todos)} todos ({completed_count} complete, {incomplete_count} incomplete)")


def main():
    """Run the demo."""
    print_separator()
    print("*** TODO CLI APPLICATION DEMO ***")
    print_separator()

    # Setup
    print("\n[*] Initializing application...")
    logger = setup_logger(name="demo", log_file="demo.log")
    storage = InMemoryStorage()
    service = TodoService(storage=storage, logger=logger)
    print("[OK] Application initialized successfully!")

    # User Story 1: Add and view todos
    print_separator()
    print("[USER STORY 1] Adding Todos")
    print_separator()

    print("\n> Adding todo: 'Buy groceries'")
    todo1 = service.create_todo("Buy groceries")
    print(f"  [OK] Created: [ID={todo1.id}] {todo1.description}")

    print("\n> Adding todo: 'Finish Phase I implementation'")
    todo2 = service.create_todo("Finish Phase I implementation")
    print(f"  [OK] Created: [ID={todo2.id}] {todo2.description}")

    print("\n> Adding todo: 'Write documentation'")
    todo3 = service.create_todo("Write documentation")
    print(f"  [OK] Created: [ID={todo3.id}] {todo3.description}")

    print("\n> Adding todo: 'Call mom'")
    todo4 = service.create_todo("Call mom")
    print(f"  [OK] Created: [ID={todo4.id}] {todo4.description}")

    print("\n> Adding todo: 'Review code changes'")
    todo5 = service.create_todo("Review code changes")
    print(f"  [OK] Created: [ID={todo5.id}] {todo5.description}")

    print("\n> Viewing all todos:")
    all_todos = service.get_all_todos()
    print_todos_table(all_todos, "All Todos")

    # User Story 2: Mark complete/incomplete
    print_separator()
    print("[USER STORY 2] Mark Complete/Incomplete")
    print_separator()

    print(f"\n> Marking todo {todo1.id} ('{todo1.description}') as complete")
    service.mark_complete(todo1.id)
    print("  [OK] Marked as complete")

    print(f"\n> Marking todo {todo2.id} ('{todo2.description}') as complete")
    service.mark_complete(todo2.id)
    print("  [OK] Marked as complete")

    print(f"\n> Marking todo {todo4.id} ('{todo4.description}') as complete")
    service.mark_complete(todo4.id)
    print("  [OK] Marked as complete")

    print("\n> Viewing all todos (with completion status):")
    all_todos = service.get_all_todos()
    print_todos_table(all_todos, "All Todos")

    # User Story 3: Filter by status
    print_separator()
    print("[USER STORY 3] Filter Todos")
    print_separator()

    print("\n> Filtering: Show completed todos only")
    completed_todos = service.get_completed_todos()
    print_todos_table(completed_todos, "Completed Todos")

    print("\n> Filtering: Show incomplete todos only")
    incomplete_todos = service.get_incomplete_todos()
    print_todos_table(incomplete_todos, "Incomplete Todos")

    # User Story 4: Update description
    print_separator()
    print("[USER STORY 4] Update Todo")
    print_separator()

    old_desc = todo3.description
    new_desc = "Write comprehensive documentation with examples"
    print(f"\n> Updating todo {todo3.id}")
    print(f"  Old: '{old_desc}'")
    print(f"  New: '{new_desc}'")
    updated = service.update_todo(todo3.id, new_desc)
    print(f"  [OK] Updated successfully")

    print("\n> Viewing all todos (with updated description):")
    all_todos = service.get_all_todos()
    print_todos_table(all_todos, "All Todos")

    # User Story 5: Delete todo
    print_separator()
    print("[USER STORY 5] Delete Todo")
    print_separator()

    print(f"\n> Deleting todo {todo5.id} ('{todo5.description}')")
    success = service.delete_todo(todo5.id)
    if success:
        print("  [OK] Deleted successfully")

    print("\n> Viewing all todos (after deletion):")
    all_todos = service.get_all_todos()
    print_todos_table(all_todos, "All Todos")

    # Final summary
    print_separator()
    print("[FINAL SUMMARY]")
    print_separator()

    total_count = service.get_todo_count()
    completed = service.get_completed_todos()
    incomplete = service.get_incomplete_todos()

    print(f"\n[OK] Total todos: {total_count}")
    print(f"[OK] Completed: {len(completed)}")
    print(f"[OK] Incomplete: {len(incomplete)}")

    print("\n[*] All User Stories Demonstrated:")
    print("  [OK] User Story 1: Add and view todos")
    print("  [OK] User Story 2: Mark complete/incomplete")
    print("  [OK] User Story 3: Filter by status")
    print("  [OK] User Story 4: Update descriptions")
    print("  [OK] User Story 5: Delete todos")

    print_separator()
    print("*** DEMO COMPLETE! ***")
    print_separator()
    print("\nTo run the interactive CLI application, use:")
    print("  python -m src.main")
    print()


if __name__ == "__main__":
    main()
