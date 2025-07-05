#!/usr/bin/env python3

import mysql.connector
import sys
import seed 

def stream_user_ages():
    """
    connects to the database and yields individual user ages one by one.
    """
    connection = None
    cursor = None
    try:
        connection = seed.connect_to_prodev()
        if not connection:
            print("ERROR: Failed to connect to the database. Cannot stream user ages.", file=sys.stderr)
            return 
        cursor = connection.cursor(dictionary=True) 
        select_query = f"SELECT age FROM {seed.TABLE_NAME};"
        cursor.execute(select_query)

        
        for row in cursor:
            try:
                age = int(row['age'])
                yield age
            except (ValueError, KeyError):
                print(f"WARNING: Skipping row due to invalid or missing age: {row}", file=sys.stderr)
                continue

    except mysql.connector.Error as err:
        print(f"ERROR: MySQL error in stream_user_ages: {err}", file=sys.stderr)
    except Exception as e:
        print(f"FATAL ERROR: An unexpected error occurred in stream_user_ages: {e}", file=sys.stderr)
    finally:

        if cursor:
            try:
                cursor.close()
            except mysql.connector.errors.InternalError:
                pass
            except Exception as e:
                print(f"WARNING: Unexpected error during cursor close in stream_user_ages: {e}", file=sys.stderr)
        if connection:
            try:
                connection.close()
            except mysql.connector.errors.InternalError:
                pass
            except Exception as e:
                print(f"WARNING: Unexpected error during connection close in stream_user_ages: {e}", file=sys.stderr)


def calculate_average_age():
    """
    Calculates the average age of users from the stream_user_ages generator
    without loading the entire dataset into memory.
    """
    total_age = 0
    user_count = 0

    
    for age in stream_user_ages():
        total_age += age
        user_count += 1
    
    if user_count > 0:
        average_age = total_age / user_count
        print(f"Average age of users: {average_age:.2f}") 
    else:
        print("No user data found to calculate average age.")


if __name__ == "__main__":
    calculate_average_age()