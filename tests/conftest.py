import pytest
from unittest.mock import Mock

@pytest.fixture
def mock_qwen_client():
    """Mock Qwen API client for testing"""
    client = Mock()
    client.complete.return_value = {"choices": [{"message": {"content": "Test response"}}]}
    return client

@pytest.fixture
def mock_semantic_scholar():
    """Mock Semantic Scholar API responses"""
    return {
        "data": [{
            "paperId": "test123",
            "title": "Test Paper",
            "abstract": "Test abstract",
            "year": 2023,
            "authors": [{"name": "Test Author"}],
            "citationCount": 100
        }],
        "total": 1
    }

@pytest.fixture
def mock_pubmed():
    """Mock PubMed XML response"""
    return """<PubmedArticle><PMID>12345</PMID><Article><ArticleTitle>Test</ArticleTitle></Article></PubmedArticle>"""

@pytest.fixture
def temp_cache_db(tmp_path):
    """Temporary SQLite database for testing"""
    return tmp_path / "test_cache.db"
