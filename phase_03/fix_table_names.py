"""Fix all table names from plural to singular"""
import os
import re

files_to_fix = [
    "backend/routes/tasks_by_email.py",
    "backend/routes/tasks.py",
    "backend/src/api/routes/chat_simple.py"
]

print("=" * 80)
print("🔧 FIXING TABLE NAMES")
print("=" * 80)

for filepath in files_to_fix:
    if not os.path.exists(filepath):
        print(f"⚠️  File not found: {filepath}")
        continue
    
    print(f"\n📝 Fixing: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Replace table names
    content = content.replace('FROM users', 'FROM "user"')
    content = content.replace('FROM tasks', 'FROM task')
    content = content.replace('INSERT INTO tasks', 'INSERT INTO task')
    content = content.replace('UPDATE tasks', 'UPDATE task')
    content = content.replace('DELETE FROM tasks', 'DELETE FROM task')
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"   ✅ Fixed!")
    else:
        print(f"   ℹ️  No changes needed")

print("\n" + "=" * 80)
print("✅ DONE! Table names fixed")
print("=" * 80)
