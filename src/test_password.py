#test_password.py - Database Connection Tester
#This is a simple but important utility script that tests whether
#the Python code can successfully connect to your PostgreSQL database.

from sqlalchemy import create_engine, text
import urllib.parse

# Your password
password = "atlantic2026!"
encoded = urllib.parse.quote_plus(password)

print("-"*50)
print("TESTING DATABASE CONNECTION")
print("-"*50)
print(f"Raw password: {password}")
print(f"Encoded password: {encoded}")
print("-"*50)

#try to connect
try:
    engine = create_engine(f'postgresql://postgres:{encoded}@localhost:5432/postgres')
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()
        print("SUCCESS! Connected to PostgreSQL!")
        print(f"Version: {version[0]}")
        
        # Test if we can create tables
        conn.execute(text("DROP TABLE IF EXISTS connection_test;"))
        conn.execute(text("CREATE TABLE connection_test (id INTEGER, name VARCHAR(50));"))
        conn.execute(text("INSERT INTO connection_test VALUES (1, 'test');"))
        result = conn.execute(text("SELECT * FROM connection_test;"))
        print("Can create tables and insert data!")
        conn.execute(text("DROP TABLE connection_test;"))
        print("All database operations working!")
        
except Exception as e:
    print(f"Failed: {e}")

print("-"*50)