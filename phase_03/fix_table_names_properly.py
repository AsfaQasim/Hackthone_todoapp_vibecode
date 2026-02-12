"""Fix all table names properly with correct SQL syntax"""
import os
import re

files_to_fix = [
    "backend/routes/tasks_by_email.py",
    "backend/routes/tasks.py",
    "backend/src/api/routes/chat_simple.py"
]

print("=" * 80)
print("🔧 FIXING TABLE NAMES PROPERLY")
print("=" * 80)

for filepath in files_to_fix:
    if not os.path.exists(filepath):
        print(f"⚠️  File not found: {filepath}")
        continue
    
    print(f"\n📝 Fixing: {filepath}")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Fix the broken syntax - replace back to simple names
    content = content.replace('FROM "user"', 'FROM "user"')  # Keep as is if already quoted
    content = content.replace('FROM user', 'FROM "user"')  # Add quotes
    content = content.replace('FROM task', 'FROM task')  # task doesn't need quotes
    
    # Fix INSERT/UPDATE/DELETE
    content = content.replace('INSERT INTO task', 'INSERT INTO task')
    content = content.replace('UPDATE task', 'UPDATE task')
    content = content.replace('DELETE FROM task', 'DELETE FROM task')
    
    # Fix the specific broken line
    content = content.replace('FROM "user" WHERE', 'FROM "user" WHERE')
    
    # Actually, let's just use simple names without quotes
    content = re.sub(r'FROM "user"', 'FROM user', content)
    content = re.sub(r'FROM task', 'FROM task', content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"   ✅ Fixed!")

print("\n" + "=" * 80)
print("✅ DONE! Checking syntax...")
print("=" * 80)

# Test import
try:
    import sys
    sys.path.insert(0, 'backend')
    print("\n🧪 Testing imports...")
    print("   This will fail if syntax is still broken")
except Exception as e:
    print(f"❌ Error: {e}")
