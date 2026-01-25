import asyncio
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from utils.jwt_handler import verify_jwt_token, TokenData
from api.todo_storage import create_todo, get_todos_by_user, get_todo_by_id, update_todo, delete_todo
from models.todo_model import TodoCreate, TodoUpdate
from datetime import datetime

def test_user_isolation():
    print("Testing user isolation in storage layer...")
    
    # Create test users
    user1_id = "user1-test-id"
    user2_id = "user2-test-id"
    
    # Create todos for user1
    todo1_data = TodoCreate(title="User 1 Todo 1", description="First todo for user 1")
    todo2_data = TodoCreate(title="User 1 Todo 2", description="Second todo for user 1")
    
    # Create todos for user2
    todo3_data = TodoCreate(title="User 2 Todo 1", description="First todo for user 2")
    todo4_data = TodoCreate(title="User 2 Todo 2", description="Second todo for user 2")
    
    # Create todos in storage
    todo1 = create_todo(todo1_data, user1_id)
    todo2 = create_todo(todo2_data, user1_id)
    todo3 = create_todo(todo3_data, user2_id)
    todo4 = create_todo(todo4_data, user2_id)
    
    print(f"Created todos: {todo1.id}, {todo2.id}, {todo3.id}, {todo4.id}")
    
    # Test that user1 can only see their own todos
    user1_todos = get_todos_by_user(user1_id)
    user2_todos = get_todos_by_user(user2_id)
    
    print(f"\nUser 1 todos count: {len(user1_todos)} (expected: 2)")
    print(f"User 2 todos count: {len(user2_todos)} (expected: 2)")
    
    # Verify user1 only gets their own todos
    user1_todo_ids = [todo.id for todo in user1_todos]
    if todo1.id in user1_todo_ids and todo2.id in user1_todo_ids:
        print("✓ User 1 can access their own todos")
    else:
        print("✗ User 1 cannot access their own todos")
    
    if todo3.id not in user1_todo_ids and todo4.id not in user1_todo_ids:
        print("✓ User 1 cannot access user 2's todos")
    else:
        print("✗ User 1 can access user 2's todos")
    
    # Verify user2 only gets their own todos
    user2_todo_ids = [todo.id for todo in user2_todos]
    if todo3.id in user2_todo_ids and todo4.id in user2_todo_ids:
        print("✓ User 2 can access their own todos")
    else:
        print("✗ User 2 cannot access their own todos")
    
    if todo1.id not in user2_todo_ids and todo2.id not in user2_todo_ids:
        print("✓ User 2 cannot access user 1's todos")
    else:
        print("✗ User 2 can access user 1's todos")
    
    # Test accessing specific todo by ID with wrong user
    print(f"\nTesting specific todo access:")
    # User1 trying to access user2's todo should fail
    user1_access_to_todo3 = get_todo_by_id(todo3.id, user1_id)
    if user1_access_to_todo3 is None:
        print("✓ User 1 cannot access user 2's specific todo")
    else:
        print("✗ User 1 can access user 2's specific todo")
    
    # User2 trying to access user2's todo should succeed
    user2_access_to_todo3 = get_todo_by_id(todo3.id, user2_id)
    if user2_access_to_todo3 is not None and user2_access_to_todo3.id == todo3.id:
        print("✓ User 2 can access their own specific todo")
    else:
        print("✗ User 2 cannot access their own specific todo")
    
    # Test update isolation
    print(f"\nTesting update isolation:")
    update_data = TodoUpdate(title="Updated Todo")
    # User1 trying to update user2's todo should fail
    update_result = update_todo(todo3.id, update_data, user1_id)
    if update_result is None:
        print("✓ User 1 cannot update user 2's todo")
    else:
        print("✗ User 1 can update user 2's todo")
    
    # User2 trying to update their own todo should succeed
    update_result = update_todo(todo3.id, update_data, user2_id)
    if update_result is not None and update_result.title == "Updated Todo":
        print("✓ User 2 can update their own todo")
    else:
        print("✗ User 2 cannot update their own todo")
    
    # Test delete isolation
    print(f"\nTesting delete isolation:")
    # User1 trying to delete user2's todo should fail
    delete_result = delete_todo(todo4.id, user1_id)
    if not delete_result:
        print("✓ User 1 cannot delete user 2's todo")
    else:
        print("✗ User 1 can delete user 2's todo")
    
    # User2 trying to delete their own todo should succeed
    original_count = len(get_todos_by_user(user2_id))
    delete_result = delete_todo(todo4.id, user2_id)
    new_count = len(get_todos_by_user(user2_id))
    if delete_result and new_count == original_count - 1:
        print("✓ User 2 can delete their own todo")
    else:
        print("✗ User 2 cannot delete their own todo")
    
    print("\nUser isolation test completed!")

if __name__ == "__main__":
    test_user_isolation()