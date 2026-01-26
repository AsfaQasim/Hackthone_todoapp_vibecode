import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('F:/hackthone_todo_vibecode/phase_03/backend/todo_app_local.db')
cursor = conn.cursor()

# Get the schema of the users table
cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='users';")
table_info = cursor.fetchone()
print("Users table schema:")
print(table_info[0] if table_info else "Table not found")

# Get all users
cursor.execute("SELECT * FROM users;")
users = cursor.fetchall()
print("\nUsers in database:")
for user in users:
    print(user)

conn.close()