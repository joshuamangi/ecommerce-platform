# Middleware for controlled chaos
import asyncio
import time
import random
import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException, status

logger = structlog.get_logger(__name__)

class ChaosMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, service_name: str, settings):
        super().__init__(app)

        self.service = service_name
        self.settings = settings

    async def dispatch(self, request, call_next):
        # intercept the request and inject controlled chaos
        # check if CHAOS.ENABLED is true
        if not self.settings.CHAOS_ENABLED:
            return await call_next(request)
        
        if random.random() < self.settings.CHAOS_PROBABILITY:
            mode = self.settings.CHAOSE_MODE.lower()

            # # # # # # # LATENCY
            if mode == "latency":
                delay = random.uniform(1,self.settings.CHAOS_MAX_DELAY)

                logger.warning("Chaos injected", chaos_type="latency", 
                               delay=round(delay,2),path=request.url.path)
            # # # # # # # HTTP 500
            elif mode == "http500":
                logger.warning("Chaos injected", chaos_type="http500",
                               path=request.url.path)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Chaos Middleware injected HTTP 500"
                )
            # configure timeout
            elif mode == "timeout":
                logger.warning("Chaos injected", chaos_type="timeout",
                               path=request.url.path)
                await asyncio.sleep(30)
            # configure exception
            elif mode == "exception":
                logger.warning("Chaos injected", chaos_type="exception",
                               path=request.url.path)
                raise RuntimeError("Chaos Middleware exception")
        return await call_next(request)
