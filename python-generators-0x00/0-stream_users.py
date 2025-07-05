#!/usr/bin/env python3

import mysql.connector
import sys

# Import the seed module to reuse its database connection function
import seed 

def stream_users():
    """
    Connects to the ALX_prodev database and streams rows from the user_data table
    one by one using a Python generator. Each row is yielded as a dictionary.
    """
    connection = None
    cursor = None
    try:
        connection = seed.connect_to_prodev()
        if not connection:
            print("Failed to connect to the database. Cannot stream users.")
            return 

      
        cursor = connection.cursor(dictionary=True) 
        
        select_query = f"SELECT user_id, name, email, age FROM {seed.TABLE_NAME};"
        cursor.execute(select_query)

        for row in cursor:
            yield row # Yield each fetched row

    except mysql.connector.Error as err:
        print(f"Error streaming user data: {err}")
        # Optionally re-raise the exception or yield an error indicator
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        
        if cursor:
            try:
            
                cursor.close() 
            except mysql.connector.errors.InternalError as e:
                
                pass # Silently ignore this known issue for partial generator consumption
            except Exception as e:
                print(f"Warning: Unexpected error during cursor close: {e}")

        if connection:
            try:
                connection.close()
            except mysql.connector.errors.InternalError as e:
                
                pass 
            except Exception as e:
                print(f"Warning: Unexpected error during connection close: {e}")

        