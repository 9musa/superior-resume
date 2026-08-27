import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]

pool: asyncpg.Pool

async def init_db_pool():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=5)

async def get_pool() -> asyncpg.Pool:
    return pool

async def get_user_by_email(email: str):
    return await pool.fetchrow("SELECT * FROM users WHERE email = $1", email)

async def create_user(email: str, password_hash: str) -> str:
    row = await pool.fetchrow(
        "INSERT INTO users (email, password_hash) VALUES ($1, $2) RETURNING id",
        email, password_hash,
    )
    return str(row["id"])