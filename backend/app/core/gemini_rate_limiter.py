import time
import threading

class GeminiRateLimiter:
    def __init__(self, rate_limit_per_minute: int = 60):
        self.lock = threading.Lock()
        self.interval = 60.0 / rate_limit_per_minute  # seconds between requests
        self.last_called = 0.0

    def wait(self):
        with self.lock:
            now = time.time()
            wait_time = self.interval - (now - self.last_called)
            if wait_time > 0:
                time.sleep(wait_time)
            self.last_called = time.time()
