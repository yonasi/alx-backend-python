import sqlite3
import functools
import os
import sys
from datetime import datetime
# This part creates a temporary database for demonstration purposes.
DB_FILE = "users.db"
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)

try:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    # Create a 'users' table
    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    );
    """)
    # Insert some sample data
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ('Yonas Mamo', 'yonasma@gmail.com'))
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ('Yonas21 Mamo21', 'yonas2121@gmail.com'))
    conn.commit()
except sqlite3.Error as e:
    print(f"Database error: {e}", file=sys.stderr)
    sys.exit(1)
finally:
    if conn:
        conn.close()
# closes connection after inserting data


def log_queries(func):
    """
    A decorator that logs the SQL query of a function before executing it.
    """
    @functools.wraps(func)
    def wrapper_log_queries(*args, **kwargs):
        """
        The wrapper function that performs the logging.
        """
        sql_query = kwargs.get('query')
        if not sql_query and args:
            sql_query = args[0]

        # Print the log message if a query was found.
        if sql_query:
            print(f'[LOG] Running query: "{sql_query}"')
        else:
            print("[LOG] Could not determine the query to log.")

        # Execute the original, decorated function and return its result.
        return func(*args, **kwargs)
    return wrapper_log_queries


@log_queries
def fetch_all_users(query: str):
    """
    Connects to the database and executes the given query to fetch users.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        return results
    except sqlite3.Error as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        return []


print("--- Fetching all users ---")
users = fetch_all_users(query="SELECT * FROM users;")
print("\nFetched Results:")
for user in users:
    print(user)

print("\n--- Fetching a single user ---")
user = fetch_all_users("SELECT * FROM users WHERE id = 1;")
print("\nFetched Results:")
print(user)


# This part removes the temporary database file.
if os.path.exists(DB_FILE):
    os.remove(DB_FILE)