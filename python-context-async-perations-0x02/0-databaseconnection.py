#!/usr/bin/env python3
import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        # Establish connection and create cursor
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        # Commit if no exceptions, rollback otherwise
        if self.connection:
            if exc_type is None:
                self.connection.commit()
            else:
                self.connection.rollback()
            self.connection.close()

if __name__ == "__main__":
    db_path = "my_database.db"
    
    with DatabaseConnection(db_path) as cursor:
        cursor.execute("SELECT * FROM users")  
        rows = cursor.fetchall()
        for row in rows:
            print(row)

