#!/usr/bin/env python3

import mysql.connector
import csv
import sys
import uuid 

# --- Configuration ---
DB_HOST = "localhost" 
DB_USER = "root"
DB_PASSWORD = "Yn@0949753643"
DB_NAME = "ALX_prodev"
TABLE_NAME = "user_data"
# --- End Configuration ---

def connect_db():
    """
    Returns a connection object if successful, None otherwise.
    """
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        print("Successfully connected to MySQL server.")
        return connection
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Access denied. Check your username and password.")
        elif err.errno == mysql.connector.errorcode.CR_CONN_ERROR:
            print(f"Error: Could not connect to MySQL server at {DB_HOST}. Is the server running?")
        else:
            print(f"An unexpected MySQL connection error occurred: {err}")
        return None

def create_database(connection):
    """
    Creates the database ALX_prodev if it does not exist.
    Requires a connection to the MySQL server.
    """
    if not connection:
        print("Error: No database connection provided to create database.")
        return

    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
        connection.commit() # Commit the database creation
        print(f"Database '{DB_NAME}' created or already exists.")
    except mysql.connector.Error as err:
        print(f"Error creating database '{DB_NAME}': {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()

def connect_to_prodev():
    """
    Connects to the ALX_prodev database in MySQL.
    Returns a connection object if successful, None otherwise.
    """
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME # Specify the database now
        )
        print(f"Successfully connected to database '{DB_NAME}'.")
        return connection
    except mysql.connector.Error as err:
        if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            print(f"Error: Database '{DB_NAME}' does not exist. Please create it first.")
        else:
            print(f"An unexpected MySQL connection error occurred when connecting to '{DB_NAME}': {err}")
        return None

def create_table(connection):
    """
    Creates a table user_data if it does not exist with the required fields.
    Requires a connection to the ALX_prodev database.
    """
    if not connection:
        print("Error: No database connection provided to create table.")
        return

    try:
        cursor = connection.cursor()
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            user_id VARCHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age INT NOT NULL
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print(f"Table '{TABLE_NAME}' created successfully or already exists.")
    except mysql.connector.Error as err:
        print(f"Error creating table '{TABLE_NAME}': {err}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()

def insert_data(connection, data_file):
    """
    Inserts data from the specified CSV file into the user_data table.
    It generates a UUID for each row and checks if a row with that UUID
    already exists before insertion.
    Requires a connection to the ALX_prodev database.
    """
    if not connection:
        print("Error: No database connection provided to insert data.")
        return

    try:
        cursor = connection.cursor()
        inserted_count = 0
        skipped_count = 0

        with open(data_file, mode='r', encoding='utf-8') as file:
            
            fieldnames = ['name', 'email', 'age'] 
            reader = csv.DictReader(file, fieldnames=fieldnames)
            
        
            try:
                
                first_row = next(reader)
                
                if any(k.lower() in ['name', 'email', 'age'] for k in first_row.values()):
                    print("Info: Skipping first row, assuming it's a header for existing fields.")
                else:
                    
                    temp_list = [first_row]
                    for row in reader:
                        temp_list.append(row)
                    reader = temp_list.__iter__() # Recreate iterator for all rows
                    
            except StopIteration:
                print("Warning: CSV file is empty.")
                return # Exit if file is empty

            data_to_insert = []
            
            for row in reader:
                # Generate a new UUID for each row
                user_id = str(uuid.uuid4()) 
                
                name = row.get('name')
                email = row.get('email')
                age = row.get('age')

                if not all([name, email, age]): # user_id is now generated, so don't check for it here
                    print(f"Warning: Skipping row due to missing data (name, email, or age): {row}")
                    continue

                try:
                    age = int(age) # Convert age to integer
                except ValueError:
                    print(f"Warning: Skipping row with generated ID '{user_id}' due to invalid age: '{age}'")
                    continue

            
                check_query = f"SELECT user_id FROM {TABLE_NAME} WHERE user_id = %s;"
                cursor.execute(check_query, (user_id,))
                if cursor.fetchone():
                   
                    print(f"Info: Generated user ID '{user_id}' already exists in DB (collision or previous run). Skipping insertion.")
                    skipped_count += 1
                else:
                    data_to_insert.append((user_id, name, email, age))
                    
            if data_to_insert:
                insert_query = f"INSERT INTO {TABLE_NAME} (user_id, name, email, age) VALUES (%s, %s, %s, %s);"
                cursor.executemany(insert_query, data_to_insert)
                connection.commit()
                inserted_count = len(data_to_insert)
                print(f"Successfully inserted {inserted_count} new rows into '{TABLE_NAME}'.")
            else:
                print("No new data found to insert (either CSV was empty after header, or age parsing failed for all).")
            
            if skipped_count > 0:
                print(f"Skipped {skipped_count} generated IDs that already existed in '{TABLE_NAME}'.")

    except FileNotFoundError:
        print(f"Error: The data file '{data_file}' was not found.")
        sys.exit(1)
    except mysql.connector.Error as err:
        print(f"Error inserting data into '{TABLE_NAME}': {err}")
        connection.rollback()
    except Exception as e:
        print(f"An unexpected error occurred during data insertion: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()