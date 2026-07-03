from prometheus_client import Counter, Histogram, Gauge

REQUEST_COUNT = Counter("http_requests_total",
                        "Total HTTP Requests", ["service","method", "endpoint", "status"])

REQUEST_LATENCY = Histogram("http_request_duration_seconds",
                            "HTTP Request Latnecy", ["service","method", "endpoint"])

ACTIVE_REQUESTS = Gauge("http_requests_in_progress", 
                        "Current request being processed", ["service"])
