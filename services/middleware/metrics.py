from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter("catalogue_http_requests_total",
                        "Total HTTP Requests", ["method", "endpoint", "status"])

REQUEST_LATENCY = Histogram("catalogue_http_request_duration_seconds",
                            "HTTP Request Latnecy", ["method", "endpoint"])
