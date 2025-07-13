#!/usr/bin/env python3
import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.connection = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        # Establish connection and execute query
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        self.results = self.cursor.fetchall()
        return self.results

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()
            self.connection.close()

if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)
    db_path = "my_database.db"

    with ExecuteQuery(db_path, query, params) as results:
        for row in results:
            print(row)