#!/usr/bin/env python3
import asyncio
import aiosqlite

DB_NAME = "my_database.db"

async def async_fetch_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return rows

async def async_fetch_older_users():
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            rows = await cursor.fetchall()
            return rows

async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())