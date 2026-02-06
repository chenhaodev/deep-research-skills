import httpx
import asyncio
from deep_research.config import APIConfig
from deep_research.api.models import QwenResponse
from deep_research.utils.logging import get_logger

logger = get_logger(__name__)


class QwenClient:
    def __init__(self, config: APIConfig):
        self.config = config
        self.client = httpx.AsyncClient(timeout=config.timeout)
    
    async def complete(
        self,
        prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.7
    ) -> QwenResponse:
        url = f"{self.config.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.config.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = await self.client.post(url, json=payload, headers=headers)
                
                if response.status_code == 429:
                    if attempt < max_retries - 1:
                        wait_time = 2 ** attempt
                        logger.warning(f"Rate limited, retrying in {wait_time}s")
                        await asyncio.sleep(wait_time)
                        continue
                    else:
                        response.raise_for_status()
                
                if response.status_code == 401:
                    raise Exception(f"Invalid API key (401 Unauthorized)")
                
                response.raise_for_status()
                
                data = response.json()
                return QwenResponse(
                    content=data["choices"][0]["message"]["content"],
                    model=data["model"],
                    usage=data.get("usage", {})
                )
            
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429 and attempt < max_retries - 1:
                    continue
                raise
        
        raise Exception("Max retries exceeded")
    
    async def close(self):
        await self.client.aclose()
