#!/usr/bin/env python3

import mysql.connector
import sys


import seed

def stream_users_in_batches(batch_size):
    """
    Connects to the ALX_prodev database and streams rows from the user_data table

    """
    connection = None
    cursor = None
    try:
        connection = seed.connect_to_prodev()
        if not connection:
            print("Failed to connect to the database. Cannot stream users in batches.", file=sys.stderr)
            return

        cursor = connection.cursor(dictionary=True) 
        select_query = f"SELECT user_id, name, email, age FROM {seed.user_data};"
        cursor.execute(select_query)

        
        while True:
            batch = cursor.fetchmany(batch_size) # This is crucial for batching!
            if not batch:
                break
            yield batch 

    except mysql.connector.Error as err:
        print(f"Error streaming user data in batches: {err}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred in stream_users_in_batches: {e}", file=sys.stderr)
    finally:
        if cursor:
            try:
                cursor.close()
            except mysql.connector.errors.InternalError as e:
                # Silently ignore this for partial generator consumption
                pass
            except Exception as e:
                print(f"Warning: Unexpected error during cursor close in stream_users_in_batches: {e}", file=sys.stderr)
        if connection:
            try:
                connection.close()
            except mysql.connector.errors.InternalError as e:
                pass
            except Exception as e:
                print(f"Warning: Unexpected error during connection close in stream_users_in_batches: {e}", file=sys.stderr)


def batch_processing(batch_size):
    """
   filtering to include only users over the age of 25. Yields filtered users one by one.
    """
    
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user.get('age') is not None and user['age'] > 25:
                yield user
