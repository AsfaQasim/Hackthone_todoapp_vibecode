print("Starting database test...")

try:
    import os
    from dotenv import load_dotenv
    print("dotenv imported successfully")
    
    load_dotenv()
    print("Environment variables loaded")
    
    # Print the database URL
    db_url = os.getenv("DATABASE_URL", "NOT SET")
    print(f"DATABASE_URL: {db_url}")
    
    if db_url == "NOT SET" or "your_username" in db_url:
        print("ERROR: You need to set your actual Neon database URL in the .env file")
        print("Go to your Neon dashboard to get the connection string")
        exit(1)
    
    from sqlmodel import create_engine
    print("SQLModel imported successfully")
    
    engine = create_engine(db_url, echo=True)
    print("Engine created")
    
    # Test the connection
    with engine.connect() as conn:
        print("Connected to database successfully!")
        result = conn.execute("SELECT 1")
        print("Simple query executed successfully")
        
    print("Database connection test completed successfully!")
    
except ImportError as e:
    print(f"Import error: {e}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()