#!/usr/bin/env python3
"""Script to check the database schema and debug the task table structure."""

import os
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_path))
sys.path.insert(0, str(backend_path / "src"))

# Change to backend directory so config can be imported
original_cwd = os.getcwd()
os.chdir(str(backend_path))

from src.db import engine, init_db
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_database_schema():
    """Check the database schema to understand the task table structure."""
    try:
        # Get the actual database URL being used
        logger.info(f"Using database URL: {engine.url}")
        
        # Connect to the database
        with engine.connect() as conn:
            # Check if task table exists
            result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table';"))
            tables = [row[0] for row in result.fetchall()]
            logger.info(f"Tables in database: {tables}")
            
            if 'task' in tables:
                # Get table info for SQLite
                if 'sqlite' in str(engine.url):
                    result = conn.execute(text("PRAGMA table_info(task);"))
                    columns = result.fetchall()
                    logger.info("Task table structure:")
                    for i, col in enumerate(columns):
                        cid, name, type_, notnull, default, pk = col
                        logger.info(f"  {i}: {name} ({type_}) {'NOT NULL' if notnull else ''} {'PK' if pk else ''}")
                        
                    # Get a sample row to understand data structure
                    result = conn.execute(text("SELECT * FROM task LIMIT 1;"))
                    sample_rows = result.fetchall()
                    
                    if sample_rows:
                        logger.info(f"Sample row data: {sample_rows[0]}")
                        logger.info(f"Number of columns in sample: {len(sample_rows[0])}")
                    else:
                        logger.info("No rows found in task table")
                else:
                    # For PostgreSQL, use different query
                    result = conn.execute(text("""
                        SELECT column_name, data_type, is_nullable, column_default
                        FROM information_schema.columns 
                        WHERE table_name = 'task' 
                        ORDER BY ordinal_position;
                    """))
                    columns = result.fetchall()
                    logger.info("Task table structure:")
                    for i, (name, dtype, nullable, default) in enumerate(columns):
                        logger.info(f"  {i}: {name} ({dtype}) {nullable} {default}")
            else:
                logger.warning("Task table does not exist in the database")
                
            if 'user' in tables:
                logger.info("\nUser table structure:")
                if 'sqlite' in str(engine.url):
                    result = conn.execute(text("PRAGMA table_info(user);"))
                    columns = result.fetchall()
                    for i, col in enumerate(columns):
                        cid, name, type_, notnull, default, pk = col
                        logger.info(f"  {i}: {name} ({type_}) {'NOT NULL' if notnull else ''} {'PK' if pk else ''}")
                else:
                    result = conn.execute(text("""
                        SELECT column_name, data_type, is_nullable, column_default
                        FROM information_schema.columns 
                        WHERE table_name = 'user' 
                        ORDER BY ordinal_position;
                    """))
                    columns = result.fetchall()
                    for i, (name, dtype, nullable, default) in enumerate(columns):
                        logger.info(f"  {i}: {name} ({dtype}) {nullable} {default}")
                        
    except Exception as e:
        logger.error(f"Error checking database schema: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Initialize the database first
    try:
        init_db()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Error initializing database: {e}")
        import traceback
        traceback.print_exc()
    
    check_database_schema()
    
    # Change back to original directory
    os.chdir(original_cwd)