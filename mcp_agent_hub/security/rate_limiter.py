"""
Sliding window rate limiter for MCP tool calls.
"""
import time
from collections import defaultdict
from typing import Dict, List

class SlidingWindowRateLimiter:
    def __init__(self, max_requests: int = 60, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, List[float]] = defaultdict(list)

    def is_allowed(self, client_id: str = "default") -> bool:
        now = time.time()
        window_start = now - self.window_seconds
        # Clean older entries
        self.requests[client_id] = [t for t in self.requests[client_id] if t > window_start]
        if len(self.requests[client_id]) >= self.max_requests:
            return False
        self.requests[client_id].append(now)
        return True

rate_limiter = SlidingWindowRateLimiter()
