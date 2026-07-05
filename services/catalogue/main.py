from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import catalogue_route
from services.middleware.monitoring import MetricsMiddleware
from services.middleware.logging import LoggingMiddleware
from services.middleware.structlog_config import configure_logging

from prometheus_client import make_asgi_app

from data.redis import redis_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await redis_client.aclose()

configure_logging("catalogue")

app = FastAPI(lifespan=lifespan)
app.add_middleware(LoggingMiddleware, service_name="catalogue")
app.add_middleware(MetricsMiddleware, service_name="catalogue")

app.include_router(catalogue_route.router)
metrics_app = make_asgi_app()

app.mount("/metrics", metrics_app)
