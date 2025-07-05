#!/usr/bin/env python3
from itertools import islice
stream_users_module = __import__('0-stream_users') 
stream_users = stream_users_module.stream_users    


for user in islice(stream_users(), 6):
    print(user)