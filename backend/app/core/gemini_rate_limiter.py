# app/core/gemini_rate_limiter.py
import time
import threading
from collections import defaultdict

class GeminiRateLimiter:
    _locks = defaultdict(threading.Lock)
    _last_called = defaultdict(float)
    _intervals = {}

    def __init__(self, rate_limit_per_minute: int = 60):
        self.default_interval = 60.0 / rate_limit_per_minute

    def wait(self, key: str):
        """Enforces rate limit per key (e.g., 'alpha', 'beta')"""
        interval = GeminiRateLimiter._intervals.get(key, self.default_interval)
        lock = GeminiRateLimiter._locks[key]

        with lock:
            now = time.time()
            last = GeminiRateLimiter._last_called.get(key, 0.0)
            wait_time = interval - (now - last)
            if wait_time > 0:
                print(f"[RateLimiter:{key}] Sleeping for {wait_time:.2f}s")
                time.sleep(wait_time)
            GeminiRateLimiter._last_called[key] = time.time()

    def set_interval_for_key(self, key: str, rate_limit_per_minute: int):
        GeminiRateLimiter._intervals[key] = 60.0 / rate_limit_per_minute
