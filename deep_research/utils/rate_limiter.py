import asyncio
import time
from typing import Optional


class RateLimiter:
    def __init__(self, calls_per_second: float):
        self.calls_per_second = calls_per_second
        self.min_interval = 1.0 / calls_per_second
        self.last_call: Optional[float] = None
        self._lock = asyncio.Lock()
    
    async def __aenter__(self):
        async with self._lock:
            if self.last_call is not None:
                elapsed = time.time() - self.last_call
                if elapsed < self.min_interval:
                    await asyncio.sleep(self.min_interval - elapsed)
            self.last_call = time.time()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass
