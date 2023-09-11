from fastapi import FastAPI, Query
import asyncpg
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

async def connect_to_db():
    conn = await asyncpg.connect(
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    return conn

@app.get("/essence/like")
async def run_query(essence_title: str = Query(...), limit: int = 50, offset: int = 0):
    conn = await connect_to_db()
    essence_title = f"%{essence_title}%"  # Wildcards for LIKE query
    query = """SELECT pe.essence_title, p.id, p.title as product_title, 'https://basalam.com/p/' || p.id as url
               FROM product_essences pe
               JOIN products p ON pe.product_id = p.id
               WHERE pe.essence_title LIKE $1
               ORDER BY pe.essence_title, p.id desc
               LIMIT $2 OFFSET $3"""
    results = await conn.fetch(query, essence_title, limit, offset)
    await conn.close()
    return results

@app.get("/essence/exact")
async def run_query(essence_title: str = Query(...), limit: int = 50, offset: int = 0):
    conn = await connect_to_db()
    query = """SELECT pe.essence_title, p.id, p.title as product_title, 'https://basalam.com/p/' || p.id as url
               FROM product_essences pe
               JOIN products p ON pe.product_id = p.id
               WHERE pe.essence_title = $1
               ORDER BY pe.essence_title, p.id desc
               LIMIT $2 OFFSET $3"""
    results = await conn.fetch(query, essence_title, limit, offset)
    await conn.close()
    return results
