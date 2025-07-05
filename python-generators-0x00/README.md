# Project Objective Clarification
The main goal is to demonstrate the use of Python generators for efficient data processing, specifically when dealing with large datasets from a MySQL database. Instead of loading all rows into memory at once (which can be memory-intensive for large tables), a generator will fetch and yield rows one by one.

`seed.py` script has a foundational role: it's responsible for setting up the database environment so that your main application can then use a generator to read from it.


# Clarification for 0-stream_users.py
The goal is to create a Python generator function stream_users() that efficiently fetches data from your ALX_prodev.user_data table one row at a time. This is crucial for handling large datasets without loading the entire table into memory, preventing memory exhaustion.