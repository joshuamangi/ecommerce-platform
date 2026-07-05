import time
from starlette.middleware.base import BaseHTTPMiddleware
from services.middleware.structlog_config import configure_logging

class LoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self,app,service_name):
        super().__init__(app)
        self.logger = configure_logging(service_name=service_name)
    
    async def dispatch(self, request, call_next):
        start = time.perf_counter()
        
        response = await call_next(request)

        duration = time.perf_counter() - start

        self.logger.info(
            "request",
            method=request.method,
            path=request.url.path,
            status=response.status_code,
            duration=duration
        )
        return response