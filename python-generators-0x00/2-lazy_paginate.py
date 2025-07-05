#!/usr/bin/env python3

import mysql.connector
import sys
import seed 

def paginate_users(page_size, offset):
    
    connection = None
    cursor = None
    rows = []
    try:
        connection = seed.connect_to_prodev()
        if not connection:
            
            print("ERROR: Failed to connect to database for pagination.", file=sys.stderr)
            return [] 
        cursor = connection.cursor(dictionary=True)
        
        cursor.execute(f"SELECT * FROM user_data LIMIT {int(page_size)} OFFSET {int(offset)}")
        rows = cursor.fetchall() 

    except mysql.connector.Error as err:
        print(f"ERROR: MySQL error in paginate_users: {err}", file=sys.stderr)
    except Exception as e:
        print(f"FATAL ERROR: An unexpected error occurred in paginate_users: {e}", file=sys.stderr)
    finally:
        if cursor:
            try:
                cursor.close()
            except mysql.connector.errors.InternalError:
                pass 
            except Exception as e:
                print(f"WARNING: Unexpected error during cursor close in paginate_users: {e}", file=sys.stderr)
        if connection:
            try:
                connection.close()
            except mysql.connector.errors.InternalError:
                pass 
            except Exception as e:
                print(f"WARNING: Unexpected error during connection close in paginate_users: {e}", file=sys.stderr)
    return rows


def lazy_paginate(page_size):
    """
    A generator function that lazily loads pages of user data from the database.
    It fetches the next page only when requested.
    """
    current_offset = 0
    
    while True:
        
        page_data = paginate_users(page_size, current_offset)
        
        if not page_data:
            break 
            
        yield page_data
        
        current_offset += page_size