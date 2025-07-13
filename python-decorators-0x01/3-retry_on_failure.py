import time
import sqlite3
import functools

# --- Prerequisite Decorator ---
def with_db_connection(func):
    """
    Decorator to automatically handle database connections.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # The database file will be created in the current directory
        conn = sqlite3.connect('users.db')
        try:
            # Pass the connection object as the first argument to the decorated function
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
            # print("Database connection closed.") # Optional: for debugging
    return wrapper


# --- Solution: retry_on_failure Decorator ---
def retry_on_failure(retries=3, delay=1):
    """
    A decorator factory that retries a function if it raises an exception.

    Args:
        retries (int): The number of times to retry the function.
        delay (int): The number of seconds to wait between retries.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {i + 1} of {retries} failed: {e}")
                    if i < retries - 1:
                        print(f"Retrying in {delay} second(s)...")
                        time.sleep(delay)
                    else:
                        print("All retries failed.")
                        raise # Re-raise the last exception
            return None # Should not be reached if retries > 0
        return wrapper
    return decorator


# --- Example Usage ---
def setup_database():
    """Sets up a dummy database for testing."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    )
    """)
    cursor.execute("INSERT INTO users (name) VALUES ('Alice')")
    cursor.execute("INSERT INTO users (name) VALUES ('Bob')")
    conn.commit()
    conn.close()

# A flag to simulate a transient error
should_fail = True

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """
    Fetches users, simulating a failure on the first attempt.
    """
    global should_fail
    if should_fail:
        should_fail = False # Ensure it only fails once
        # Simulate a database lock or temporary error
        raise sqlite3.OperationalError("database is locked")
    
    print("Successfully connected and fetched users.")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()

if __name__ == "__main__":
    setup_database()
    print("--- Attempting to fetch users with automatic retry on failure ---")
    users = fetch_users_with_retry()
    print("\n--- Fetched Users ---")
    print(users)