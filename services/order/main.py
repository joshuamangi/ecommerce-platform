from contextlib import asynccontextmanager
from data.redis import redis_client
from fastapi import FastAPI

from routers import order_route


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await redis_client.aclose()

app = FastAPI(lifespan=lifespan)

app.include_router(order_route.router)
