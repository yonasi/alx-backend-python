import sqlite3
import functools

def with_db_connection(func):
    """
    Decorator to automatically handle database connections.
    It opens a connection, passes it to the function, and closes it afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            # Pass the connection object as the first argument
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

# --- Example Usage ---

def setup_database():
    """Sets up a dummy database for testing."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("""
    CREATE TABLE users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )
    """)
    cursor.execute("INSERT INTO users (name, email) VALUES ('John Doe', 'john.doe@example.com')")
    conn.commit()
    conn.close()

@with_db_connection
def get_user_by_id(conn, user_id):
    """Fetches a user by their ID from the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

if __name__ == "__main__":
    setup_database()
    # Fetch user by ID with automatic connection handling
    user = get_user_by_id(user_id=1)
    print(user)