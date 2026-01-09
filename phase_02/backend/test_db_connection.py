import os
import sys
from dotenv import load_dotenv

print("Loading environment variables...")
load_dotenv()

db_url = os.getenv("DATABASE_URL")
print(f"Database URL: {db_url}")

if not db_url or "your_" in db_url:
    print("ERROR: Database URL not properly configured!")
    sys.exit(1)

try:
    from sqlmodel import create_engine, SQLModel
    from models.task_model import Task
    
    print("Creating engine...")
    engine = create_engine(db_url, echo=True)
    
    print("Testing connection...")
    with engine.connect() as conn:
        print("Connected successfully!")
        result = conn.execute("SELECT 1;")
        print("Query executed successfully")
    
    print("Creating tables...")
    SQLModel.metadata.create_all(engine)
    print("Tables created successfully!")
    
    # Verify tables exist
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Tables in database: {tables}")
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()