import aiosqlite
import asyncio

async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            return users

async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            older_users = await cursor.fetchall()
            return older_users

async def fetch_concurrently():
    await asyncio.gather(
        fetch_users(),
        fetch_older_users()
    )

if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
# This code uses aiosqlite to fetch users and older users concurrently from a SQLite database.
# Ensure you have a SQLite database named "users.db" with a table "users" containing the necessary data.