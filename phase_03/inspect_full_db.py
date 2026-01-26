import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('F:/hackthone_todo_vibecode/phase_03/backend/todo_app_local.db')
cursor = conn.cursor()

# Get all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables in database:")
for table in tables:
    print(f"- {table[0]}")

print()

# Get the schema of all tables
for table_name in [table[0] for table in tables]:
    cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
    table_info = cursor.fetchone()
    print(f"{table_name} table schema:")
    print(table_info[0] if table_info else "Table not found")
    print()

# Get all records from all tables
for table_name in [table[0] for table in tables]:
    print(f"Records in {table_name}:")
    cursor.execute(f"SELECT * FROM {table_name};")
    records = cursor.fetchall()
    for record in records:
        print(record)
    print()

conn.close()