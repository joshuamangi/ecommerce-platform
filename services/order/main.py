from contextlib import asynccontextmanager
from data.redis import redis_client
from fastapi import FastAPI
from services.middleware.monitoring import MetricsMiddleware
from prometheus_client import make_asgi_app

from routers import order_route


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await redis_client.aclose()

app = FastAPI(lifespan=lifespan)

app.add_middleware(MetricsMiddleware, service_name="orders")
app.include_router(order_route.router)

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)