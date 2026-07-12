# Cricuit breaker class
# Defines close, open and half open and open scenrarios for when faults occur

# If error occurs open circuit
# Try if it open, if the failure timeout time is greater than last_timeout minus current time then half open
# If circuit is closed then call the function and reset the failure count and set the state to closed

import time


class CircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_timeout=5):
        self.state = "CLOSED"
        self.failures = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.last_failure_time = None

    async def call(self,func,*args, **kwargs):
        if self.state == "OPEN":
            if time.time() - self.last_failure_time >= self.recovery_timeout:
                self.state = "HALF_OPEN"
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
        if self.failures >= self.failure_threshold:
            self.state = "OPEN"

    def reset(self):
        self.failures = 0
        self.state = "CLOSED"
