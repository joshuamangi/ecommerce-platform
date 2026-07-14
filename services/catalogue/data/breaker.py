from services.common.circuit_breaker.circuit_breaker import CircuitBreaker

database_breaker = CircuitBreaker(
    failure_threshold=3,
    recovery_timeout=10
)