import time
from starlette.middleware.base import BaseHTTPMiddleware
from services.middleware.metrics import REQUEST_COUNT, REQUEST_LATENCY


class MetricsMiddleware(BaseHTTPMiddleware):
    # define method that gets the request and the callnext callback
    async def dispatch(self, request, call_next):
        # start counter
        start = time.perf_counter()
        # get response
        response = await call_next(request)
        # duration calculation
        duration = time.perf_counter() - start
        # Add response to label
        REQUEST_COUNT.labels(request.method, request.url.path,
                             response.status_code,).inc()
        # Add response to label
        REQUEST_LATENCY.labels(
            request.method, request.url.path,).observe(duration)
        return response
