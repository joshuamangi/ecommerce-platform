import sys
from routers import auth_route

from fastapi import FastAPI
from services.middleware.monitoring import MetricsMiddleware
from services.middleware.logging import LoggingMiddleware
from services.middleware.structlog_config import configure_logging
from prometheus_client import make_asgi_app

print("System Path", sys.path)

configure_logging("auth")

app = FastAPI()
app.add_middleware(LoggingMiddleware, service_name="auth")
app.add_middleware(MetricsMiddleware, service_name="auth")

app.include_router(auth_route.router)

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)