import asyncio

import orjson
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from fastapi import Depends
from sqlalchemy import select
from data.models import Catalogue
from schema.catalogue_schema import CatalogueOut
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


async def update_catalogue(id: int, catalogue: CatalogueOut):
    async with SessionLocal() as db:
        key = f"catalogue:{id}:data"
        # Check if the product exists
        result = await db.execute(select(Catalogue).where(Catalogue.id == id))
        item = result.scalars().one_or_none()

        if not item:
            return None
        item.id = catalogue.id
        item.sku = catalogue.sku
        item.description = catalogue.description
        item.price = catalogue.price
        item.name = catalogue.name

        await db.commit()
        await db.refresh(item)

        await redis_client.delete(key)

        # Update the record if it exists
        # DELETE the cache


# For 1000 requests
# async def run_benchmark():
#     target_id = 1
#     total_requests = 1000
#     latencies = []
#     for i in range(total_requests):
#         duration, hit = await fetch_catalogue(target_id)
#         latencies.append(duration)
#         if i == 0:
#             print(f"First Request (DB): {duration:.6f}s")
#         elif i == 1:
#             print(f"Second Request (Cache): {duration:.6f}s")

#     avg_latency = sum(latencies[1:]) / (total_requests - 1)
#     print("-" * 30)
#     print(f"Total Requests: {total_requests}")
#     print(f"Average Cache Hit Latency: {avg_latency:.6f}s")
#     print(f"Total time for 1000 requests: {sum(latencies):.4f}s")


# For 6 second delay
# async def run_benchmark():
#     target_id = 1
#     # We will run fewer iterations to make the test time manageable
#     total_requests = 10

#     for i in range(total_requests):
#         # 1. Fetch with TTL (Note: change your setex to 5 seconds)
#         # Inside fetch_catalogue, change: await redis_client.setex(key, 5, ...)

#         duration, hit = await fetch_catalogue(target_id)
#         status = "Cache Hit" if hit else "DB Miss (Cache Expired or Initial)"
#         print(f"Request {i+1}: {status} | Latency: {duration:.6f}s")

#         # 2. Wait 6 seconds to force expiration (TTL is 5s)
#         if i < total_requests - 1:
#             print("--- Sleeping for 6s to trigger TTL expiration ---")
#             await asyncio.sleep(6)


# Invalidation Logic
async def invalidation_logic():
    # 1. Prime the cache
    await fetch_catalogue(id=1)

    # 2. Update DB and delete cache
    data = CatalogueOut(id=1, sku="A", name="A",
                        description="new update", price=123, stock_quantity=4)
    await update_catalogue(id=1, catalogue=data)

    # 3. Check status
    # This should be a MISS because we just deleted it
    duration, hit = await fetch_catalogue(id=1)

    if not hit:
        print("Success: Cache was cleared and we triggered a fresh DB fetch.")
    else:
        print("Failure: Cache was not cleared.")

if __name__ == "__main__":
    asyncio.run(invalidation_logic())
