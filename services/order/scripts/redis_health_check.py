import asyncio
from data.redis import redis_client


async def test_redis_connection():
    try:
        response = await redis_client.ping()
        if response:
            print("Successfully connected to Redis!")

        # Test basic read/write
        await redis_client.set("health_check", "ok")
        val = await redis_client.get("health_check")
        print(f"Redis read/write test: {val}")

    except Exception as e:
        print(f"Redis connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_redis_connection())
