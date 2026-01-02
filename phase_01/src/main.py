"""
Main entry point for the Todo CLI application.

This module sets up dependency injection and launches the CLI.
"""

import sys
from src.infrastructure.storage import InMemoryStorage
from src.infrastructure.logger import setup_logger
from src.services.todo_service import TodoService
from src.adapters.cli import CLIAdapter


def main() -> int:
    """
    Main entry point for the application.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    try:
        # Setup infrastructure
        logger = setup_logger()
        storage = InMemoryStorage()

        # Setup service layer
        service = TodoService(storage=storage, logger=logger)

        # Setup adapter layer
        cli = CLIAdapter(service=service, logger=logger)

        # Run application
        cli.run()

        return 0

    except KeyboardInterrupt:
        print("\n\nℹ️  Operation cancelled. Goodbye!")
        return 0
    except Exception as e:
        print(f"\n✗ Error: An unexpected error occurred: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
