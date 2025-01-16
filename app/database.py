import asyncpg
from fastapi import FastAPI

DATABASE_URL = "postgresql://username:password@localhost/ReservationDB"

async def get_db_connection():
    return await asyncpg.connect(DATABASE_URL)
