from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import catalogue_route
from services.middleware.monitoring import MetricsMiddleware
from prometheus_client import make_asgi_app

from data.redis import redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await redis_client.aclose()

app = FastAPI(lifespan=lifespan)
app.add_middleware(MetricsMiddleware)

app.include_router(catalogue_route.router)
metrics_app = make_asgi_app()

app.mount("/metrics", metrics_app)
