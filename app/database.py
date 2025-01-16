import asyncpg

DATABASE_URL = "postgresql://postgres:dani0919@localhost/ReservationCreateDb"

async def get_db_connection():
    return await asyncpg.connect(DATABASE_URL)
