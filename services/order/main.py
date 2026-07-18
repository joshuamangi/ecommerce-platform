from contextlib import asynccontextmanager
from data.redis import redis_client
from fastapi import FastAPI
from utils.config import settings
from services.middleware.chaos import ChaosMiddleware
from services.middleware.monitoring import MetricsMiddleware
from services.middleware.logging import LoggingMiddleware
from services.middleware.structlog_config import configure_logging




from prometheus_client import make_asgi_app

from routers import order_route


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await redis_client.aclose()

configure_logging("orders")
app = FastAPI(lifespan=lifespan)

app.add_middleware(LoggingMiddleware, service_name="orders")
app.add_middleware(ChaosMiddleware, service_name="orders", settings=settings)
app.add_middleware(MetricsMiddleware, service_name="orders")
app.include_router(order_route.router)

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)