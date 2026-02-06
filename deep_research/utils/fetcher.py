import asyncio
from typing import List, TypeVar, Callable, Awaitable

T = TypeVar('T')


async def fetch_parallel(
    items: List[T],
    fetch_func: Callable[[T], Awaitable[any]],
    max_concurrent: int = 5
) -> List[any]:
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async def bounded_fetch(item: T):
        async with semaphore:
            return await fetch_func(item)
    
    tasks = [bounded_fetch(item) for item in items]
    return await asyncio.gather(*tasks, return_exceptions=True)
