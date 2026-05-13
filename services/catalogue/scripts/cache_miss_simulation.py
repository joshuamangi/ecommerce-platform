import asyncio

import orjson
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from fastapi import Depends
from sqlalchemy import select
from data.models import Catalogue
from utils.config import settings
from redis.asyncio import Redis
from redis.asyncio.connection import ConnectionPool
from time import perf_counter

DATABASE_URL = settings.DATABASE_URL
engine = create_async_engine(DATABASE_URL)

SessionLocal = async_sessionmaker(
    bind=engine, autoflush=False, expire_on_commit=False)

redis_pool = ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)

redis_client = Redis(connection_pool=redis_pool)


async def get_db():
    async with SessionLocal() as db:
        yield db


async def fetch_catalogue(id: int):
    async with SessionLocal() as db:

        start_time = perf_counter()
        key = f"catalogue:{id}:data"
        cached_data = await redis_client.get(name=key)
        if cached_data:
            end_time = perf_counter()
            return end_time - start_time, True

        result = await db.execute(select(Catalogue).where(Catalogue.id == id))
        item = result.scalars().one_or_none()

        if item:
            data = {
                "id": item.id,
                "sku": item.sku,
                "name": item.name,
                "description": item.description,
                "price": item.price,
                "stock_quantity": item.stock_quantity
            }
            await redis_client.setex(key, 300, orjson.dumps(data))
        end_time = perf_counter()
        return end_time - start_time, False


async def run_benchmark():
    target_id = 1
    total_requests = 1000
    latencies = []
    for i in range(total_requests):
        duration, hit = await fetch_catalogue(target_id)
        latencies.append(duration)
        if i == 0:
            print(f"First Request (DB): {duration:.6f}s")
        elif i == 1:
            print(f"Second Request (Cache): {duration:.6f}s")

    avg_latency = sum(latencies[1:]) / (total_requests - 1)
    print("-" * 30)
    print(f"Total Requests: {total_requests}")
    print(f"Average Cache Hit Latency: {avg_latency:.6f}s")
    print(f"Total time for 1000 requests: {sum(latencies):.4f}s")


if __name__ == "__main__":
    asyncio.run(run_benchmark())
