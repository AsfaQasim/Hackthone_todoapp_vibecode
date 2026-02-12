"""Verify tasks exist in database"""
import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://neondb_owner:npg_6DzBwoCp1Muf@ep-holy-flower-ahrkffp6-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require')
USER_ID = "add60fd1-792f-4ab9-9a53-e2f859482c59"

engine = create_engine(DATABASE_URL)
conn = engine.connect()

# Check tasks
result = conn.execute(text('SELECT * FROM task WHERE user_id = :uid'), {'uid': USER_ID})
tasks = result.fetchall()

print(f"Tasks in database: {len(tasks)}")
for task in tasks:
    print(f"  - {task[1]} (ID: {task[4]})")
