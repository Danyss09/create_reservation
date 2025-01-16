import asyncpg

DATABASE_URL = "postgresql://postgres:dani0919@localhost/ReservationCreateDB"

async def get_db_connection():
    return await asyncpg.connect(DATABASE_URL)
