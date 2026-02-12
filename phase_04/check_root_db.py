import sqlite3

# Connect to the SQLite database in the root directory
db_path = 'F:/hackthone_todo_vibecode/phase_03/todo_app_local.db'
print(f"Checking database at: {db_path}")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Get all records from the users table
cursor.execute("SELECT * FROM users;")
records = cursor.fetchall()
print(f"Number of users in database: {len(records)}")

for record in records:
    print(f"User: ID={record[0]}, Email={record[1]}, Name={record[2]}")

conn.close()