from fastapi import FastAPI, Query, HTTPException, Depends
from enum import Enum
import asyncpg
from config import DB_CONFIG, LIMIT, OFFSET

app = FastAPI()


class Condition(Enum):
    like = "LIKE"
    exact = "="


async def get_db_pool():
    return await asyncpg.create_pool(**DB_CONFIG)


@app.on_event("startup")
async def startup():
    app.state.db_pool = await get_db_pool()


@app.on_event("shutdown")
async def shutdown():
    await app.state.db_pool.close()


async def run_query(query, *args, pool: asyncpg.Pool):
    async with pool.acquire() as conn:
        try:
            return await conn.fetch(query, *args)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Database error: {str(e)}"
            )


def get_db_pool_dependency():
    return app.state.db_pool


def build_essence_query(
    condition: Condition, essence_title: str, limit: int, offset: int
):
    if condition == Condition.like:
        essence_title = f"%{essence_title}%"

    print(condition.value)

    query = f"""
        SELECT pe.essence_title, p.id, p.title as product_title,
               'https://basalam.com/p/' || p.id as url
        FROM product_essences pe
        JOIN products p ON pe.product_id = p.id
        WHERE pe.essence_title {condition.value} $1
        ORDER BY pe.essence_title, p.id desc
        LIMIT $2 OFFSET $3
    """

    return query, [essence_title, limit, offset]


@app.get("/essence/{condition}")
async def essence_query(
    condition: Condition,
    essence_title: str = Query(...),
    limit: int = LIMIT,
    offset: int = OFFSET,
    pool: asyncpg.Pool = Depends(get_db_pool_dependency),
):
    query, params = build_essence_query(
        condition, essence_title, limit, offset
    )
    return await run_query(query, *params, pool=pool)
