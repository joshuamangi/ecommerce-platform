from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import catalogue_route

from data.redis import redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await redis_client.aclose()

app = FastAPI(lifespan=lifespan)


app.include_router(catalogue_route.router)
