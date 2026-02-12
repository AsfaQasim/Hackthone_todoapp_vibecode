"""Check what tables exist in database"""
import os
from sqlalchemy import create_engine, text, inspect

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://neondb_owner:npg_6DzBwoCp1Muf@ep-holy-flower-ahrkffp6-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require')

print("=" * 80)
print("🔍 CHECKING DATABASE SCHEMA")
print("=" * 80)

try:
    engine = create_engine(DATABASE_URL)
    inspector = inspect(engine)
    
    # Get all tables
    tables = inspector.get_table_names()
    
    print(f"\n📊 Tables in database: {len(tables)}")
    for table in tables:
        print(f"   - {table}")
        
        # Get columns for each table
        columns = inspector.get_columns(table)
        print(f"     Columns:")
        for col in columns:
            print(f"       • {col['name']} ({col['type']})")
        print()
    
    if not tables:
        print("⚠️  No tables found! Database needs to be initialized.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("=" * 80)
