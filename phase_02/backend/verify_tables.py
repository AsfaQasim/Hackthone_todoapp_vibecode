import os
from dotenv import load_dotenv
from sqlmodel import create_engine, SQLModel
from sqlalchemy import inspect

# Load environment variables
load_dotenv()

# Get database URL
db_url = os.getenv("DATABASE_URL")
print(f"Using database URL: {db_url}")

if not db_url or "your_" in db_url:
    print("ERROR: Database URL not properly configured!")
    exit(1)

# Create engine
engine = create_engine(db_url, echo=False)

# Check tables
inspector = inspect(engine)
tables = inspector.get_table_names()
print(f"Tables found in database: {tables}")

if 'task' in tables:
    print("SUCCESS: Task table exists!")
else:
    print("WARNING: Task table does not exist")

# Print table columns if task table exists
if 'task' in tables:
    columns = inspector.get_columns('task')
    print(f"Task table columns: {[col['name'] for col in columns]}")