import time
from starlette.middleware.base import BaseHTTPMiddleware
from services.middleware.metrics import REQUEST_COUNT, REQUEST_LATENCY, ACTIVE_REQUESTS


class MetricsMiddleware(BaseHTTPMiddleware):
    # define method that gets the request and the callnext callback
    def __init__(self, app, service_name:str):
        super().__init__(app)
        self.service = service_name

    async def dispatch(self, request, call_next):
        ACTIVE_REQUESTS.labels(self.service).inc()
        # start counter
        start = time.perf_counter()
        # get response
        try:
            response = await call_next(request)
            # duration calculation
            # Add response to label
            REQUEST_COUNT.labels(self.service, request.method, request.url.path,
                                response.status_code,).inc()
            return response
        finally:
            duration = time.perf_counter() - start
            # Add response to label
            REQUEST_LATENCY.labels(self.service,
                request.method, request.url.path,).observe(duration)
            ACTIVE_REQUESTS.labels(self.service).dec()
