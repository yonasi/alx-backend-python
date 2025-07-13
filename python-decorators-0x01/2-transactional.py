import sqlite3
import functools

def with_db_connection(func):
    """
    Decorator to automatically handle database connections.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

def transactional(func):
    """
    Decorator that manages database transactions by automatically
    committing or rolling back changes.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            return result
        except Exception as e:
            conn.rollback()
            print(f"Transaction failed: {e}")
            raise
    return wrapper

# --- Example Usage ---

def setup_database_for_update():
    """Sets up a dummy database for testing updates."""
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
    cursor.execute("INSERT INTO users (name, email) VALUES ('Test User', 'test@example.com')")
    conn.commit()
    conn.close()

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """Updates a user's email in the database."""
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    print(f"Successfully updated email for user {user_id}")

@with_db_connection
def get_user_email(conn, user_id):
    """Fetches a user's email by their ID."""
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()[0]


if __name__ == "__main__":
    setup_database_for_update()

    print("Initial email:", get_user_email(user_id=1))

    # Update user's email with automatic transaction handling
    update_user_email(user_id=1, new_email='Crawford_Cartwright@hotmail.com')

    print("Updated email:", get_user_email(user_id=1))