import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine
from models.task_model import Task
from utils.db import DATABASE_URL

# Load environment variables
load_dotenv()

print("Debugging Database Connection...")
print(f"DATABASE_URL: {DATABASE_URL}")

# Show the actual database URL being used
actual_db_url = os.getenv("DATABASE_URL", "postgresql://username:password@localhost/dbname")
print(f"Actual DATABASE_URL from env: {actual_db_url}")

# Create engine
try:
    engine = create_engine(actual_db_url, echo=True)
    print("Engine created successfully")
except Exception as e:
    print(f"Error creating engine: {e}")
    exit(1)

# Test connection
try:
    with engine.connect() as conn:
        print("Connected to database successfully")
        # Test with a simple query
        result = conn.execute("SELECT version();")
        print(f"Database version: {result.fetchone()[0]}")
except Exception as e:
    print(f"Error connecting to database: {e}")
    exit(1)

# Create tables
try:
    print("Creating tables...")
    SQLModel.metadata.create_all(engine)
    print("Tables created successfully!")
    
    # Verify tables exist
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Tables in database: {tables}")
    
    if 'task' in tables:
        print("✓ Task table exists!")
    else:
        print("✗ Task table does not exist")
        
except Exception as e:
    print(f"Error creating tables: {e}")
    import traceback
    traceback.print_exc()