# Cricuit breaker class
# Defines close, open and half open and open scenrarios for when faults occur

# If error occurs open circuit
# Try if it open, if the failure timeout time is greater than last_timeout minus current time then half open
# If circuit is closed then call the function and reset the failure count and set the state to closed

import time
import structlog

logger = structlog.get_logger(__name__)

class CircuitBreaker:
    def __init__(self, failure_threshold, recovery_timeout):
        self.state = "CLOSED"
        self.failures = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.last_failure_time = None

    async def call(self,func,*args, fallback_func=None, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
                if fallback_func:
                    logger.info("Circuit Breaker state is HALF OPEN")
                    return await fallback_func()
            else:
                logger.info("Circuit Breaker state is OPEN")
                return "Circuit is OPEN: Fallback response provided"
        try:
            result = await func(*args, **kwargs)
            self.reset()
            return result
        except Exception as e:
            self.handle_failure()
            raise e

    def handle_failure(self):
        self.failures += 1
        self.last_failure_time = time.time()

        logger.warning("Circuit failure", failures=self.failures, threshold=self.failure_threshold,)
        if self.failures >= self.failure_threshold:
            self.state = "OPEN"
            logger.error("Circuit opened", recovery_timeout=self.recovery_timeout,)

    def reset(self):
        self.failures = 0
        self.state = "CLOSED"
        logger.info("Circuit Breaker State is CLOSED")
