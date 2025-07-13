import time
import sqlite3
import functools

# A simple in-memory cache
query_cache = {}

# --- Prerequisite Decorator ---
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

# --- Solution: cache_query Decorator ---
def cache_query(func):
    """
    A decorator that caches the results of a query based on the SQL query string.
    """
    @functools.wraps(func)
    def wrapper(conn, query, *args, **kwargs):
        # Check if the query result is already in the cache
        if query in query_cache:
            print(f"CACHE HIT: Returning cached result for query: '{query}'")
            return query_cache[query]
        
        # If not in cache, execute the function and store the result
        print(f"CACHE MISS: Executing query and caching result for: '{query}'")
        result = func(conn, query, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

# --- Example Usage ---
def setup_database():
    """Sets up a dummy database for testing."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    cursor.execute("INSERT INTO users (name) VALUES ('Charlie')")
    cursor.execute("INSERT INTO users (name) VALUES ('Diana')")
    conn.commit()
    conn.close()

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Fetches data from the database. The result will be cached.
    """
    print("Executing database query...")
    cursor = conn.cursor()
    cursor.execute(query)
    # Simulate a delay as if the query is slow
    time.sleep(2) 
    return cursor.fetchall()

if __name__ == "__main__":
    setup_database()
    
    print("--- First call (should execute and cache) ---")
    start_time = time.time()
    users = fetch_users_with_cache(query="SELECT * FROM users")
    end_time = time.time()
    print(f"Users: {users}")
    print(f"Duration: {end_time - start_time:.2f} seconds\n")

    print("--- Second call (should use the cached result) ---")
    start_time = time.time()
    users_again = fetch_users_with_cache(query="SELECT * FROM users")
    end_time = time.time()
    print(f"Users: {users_again}")
    print(f"Duration: {end_time - start_time:.2f} seconds")
