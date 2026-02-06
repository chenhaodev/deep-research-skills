import pytest
import asyncio
from deep_research.utils.fetcher import fetch_parallel


async def mock_fetch(item: int) -> int:
    await asyncio.sleep(0.01)
    return item * 2


@pytest.mark.asyncio
async def test_fetch_parallel():
    items = [1, 2, 3, 4, 5]
    results = await fetch_parallel(items, mock_fetch, max_concurrent=3)
    
    assert len(results) == 5
    assert 2 in results
    assert 10 in results


@pytest.mark.asyncio
async def test_fetch_parallel_with_errors():
    async def failing_fetch(item: int) -> int:
        if item == 3:
            raise ValueError("Test error")
        return item * 2
    
    items = [1, 2, 3, 4]
    results = await fetch_parallel(items, failing_fetch, max_concurrent=2)
    
    assert len(results) == 4
    assert isinstance(results[2], ValueError)
