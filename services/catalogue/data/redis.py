from redis.asyncio import Redis
from redis.asyncio.connection import ConnectionPool
from utils.config import settings

redis_pool = ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True,
    max_connections=10,
)
redis_client = Redis(connection_pool=redis_pool)
