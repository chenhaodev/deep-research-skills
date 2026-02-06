import pytest
import httpx
import respx
from deep_research.api.qwen import QwenClient
from deep_research.config import APIConfig


@pytest.fixture
def qwen_config():
    return APIConfig(
        api_key="test_key",
        base_url="https://test.api.com/v1",
        model="qwen/qwen3-max"
    )


@pytest.mark.asyncio
@respx.mock
async def test_qwen_complete_success(qwen_config):
    client = QwenClient(qwen_config)
    
    respx.post("https://test.api.com/v1/chat/completions").mock(
        return_value=httpx.Response(200, json={
            "choices": [{"message": {"content": "Test response"}}],
            "model": "qwen/qwen3-max",
            "usage": {"prompt_tokens": 10, "completion_tokens": 20}
        })
    )
    
    response = await client.complete("Test prompt")
    assert response.content == "Test response"
    assert response.model == "qwen/qwen3-max"


@pytest.mark.asyncio
@respx.mock
async def test_qwen_rate_limit_retry(qwen_config):
    client = QwenClient(qwen_config)
    
    respx.post("https://test.api.com/v1/chat/completions").mock(
        side_effect=[
            httpx.Response(429, json={"error": "Rate limit"}),
            httpx.Response(200, json={
                "choices": [{"message": {"content": "Success after retry"}}],
                "model": "qwen/qwen3-max",
                "usage": {}
            })
        ]
    )
    
    response = await client.complete("Test prompt")
    assert response.content == "Success after retry"


@pytest.mark.asyncio
@respx.mock
async def test_qwen_invalid_api_key(qwen_config):
    client = QwenClient(qwen_config)
    
    respx.post("https://test.api.com/v1/chat/completions").mock(
        return_value=httpx.Response(401, json={"error": "Invalid API key"})
    )
    
    with pytest.raises(Exception, match="401|Invalid API key|Unauthorized"):
        await client.complete("Test prompt")
