from pydantic import BaseModel, Field
from pathlib import Path
import os


class APIConfig(BaseModel):
    api_key: str = Field(default_factory=lambda: os.getenv('DEEP_RESEARCH_QWEN_API_KEY', ''))
    base_url: str = "https://openrouter.ai/api/v1"
    model: str = "qwen/qwen3-max"
    timeout: int = 60


class CacheConfig(BaseModel):
    path: Path = Path.home() / ".deep-research" / "cache.db"
    ttl_days: int = 30
    enabled: bool = True


class SearchConfig(BaseModel):
    max_papers_per_query: int = 100
    max_searches_per_review: int = 25
    relevance_threshold: float = 0.6
    min_abstract_words: int = 50
    date_range_years: int = 3


class Config(BaseModel):
    qwen: APIConfig = Field(default_factory=APIConfig)
    cache: CacheConfig = Field(default_factory=CacheConfig)
    search: SearchConfig = Field(default_factory=SearchConfig)
