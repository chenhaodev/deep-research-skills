from deep_research.config import Config, APIConfig, CacheConfig, SearchConfig


def test_load_default_config():
    config = Config()
    assert config.cache.ttl_days == 30
    assert config.search.max_papers_per_query == 100
    assert config.search.relevance_threshold == 0.6


def test_env_override():
    import os
    os.environ['DEEP_RESEARCH_QWEN_API_KEY'] = 'test_key'
    config = Config()
    assert config.qwen.api_key == 'test_key'
    del os.environ['DEEP_RESEARCH_QWEN_API_KEY']
