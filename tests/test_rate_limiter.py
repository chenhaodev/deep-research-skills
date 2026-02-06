import pytest
import asyncio
import time
from deep_research.utils.rate_limiter import RateLimiter


@pytest.mark.asyncio
async def test_rate_limiter_delays():
    limiter = RateLimiter(calls_per_second=2)
    
    start = time.time()
    async with limiter:
        pass
    async with limiter:
        pass
    elapsed = time.time() - start
    
    assert elapsed >= 0.5


@pytest.mark.asyncio
async def test_rate_limiter_burst():
    limiter = RateLimiter(calls_per_second=10)
    
    start = time.time()
    tasks = [limiter.__aenter__() for _ in range(5)]
    await asyncio.gather(*tasks)
    for _ in range(5):
        await limiter.__aexit__(None, None, None)
    elapsed = time.time() - start
    
    assert elapsed < 1.0
