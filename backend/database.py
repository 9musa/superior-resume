import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]

pool: asyncpg.Pool

async def init_db_pool():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=5, timeout=30, command_timeout=30)

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

async def create_job(job_title: str, owner_id: str | None, parsed_text: str) -> str:
    row = await pool.fetchrow(
        """
        INSERT INTO jobs (owner_id, job_title, parsed_text)
        VALUES ($1, $2, $3)
        RETURNING id
        """,
        owner_id, job_title, parsed_text,
    )
    return str(row["id"])

async def get_job(job_id: str):
    return await pool.fetchrow("SELECT * FROM jobs WHERE id = $1", job_id)

async def update_job_status(job_id: str, status: str, result: str):
    await pool.execute(
        "UPDATE jobs SET status = $1, result = $2 WHERE id = $3",
        status, result, job_id
    )

async def update_job_result(job_id: str, status: str, result_text: str, result_pdf: bytes | None = None):
    await pool.execute(
        "UPDATE jobs SET status = $1, result = $2, result_pdf = $3 WHERE id = $4",
        status, result_text, result_pdf, job_id,
    )