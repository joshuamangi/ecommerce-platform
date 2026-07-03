import sys
from routers import auth_route

from fastapi import FastAPI
from services.middleware.monitoring import MetricsMiddleware
from prometheus_client import make_asgi_app

print("System Path", sys.path)

app = FastAPI()
app.add_middleware(MetricsMiddleware, service_name="orders")

app.include_router(auth_route.router)

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)