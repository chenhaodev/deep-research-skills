import pytest
from pathlib import Path
from deep_research.storage.cache import CacheManager
from deep_research.api.models import Paper, Author


def test_cache_set_and_get(tmp_path):
    """Test basic cache set and get operations."""
    cache = CacheManager(tmp_path / "test.db")
    paper = Paper(paper_id="test123", title="Test Paper")
    
    cache.set("test123", paper, "test")
    retrieved = cache.get("test123")
    
    assert retrieved is not None
    assert retrieved.paper_id == "test123"
    assert retrieved.title == "Test Paper"


def test_cache_miss(tmp_path):
    """Test cache miss returns None."""
    cache = CacheManager(tmp_path / "test.db")
    result = cache.get("nonexistent")
    assert result is None


def test_cache_expiration(tmp_path):
    """Test cache expiration based on TTL."""
    cache = CacheManager(tmp_path / "test.db")
    paper = Paper(paper_id="test123", title="Test")
    cache.set("test123", paper, "test")
    
    # Should not be expired with 30 day TTL
    assert cache.is_expired("test123", 30) is False
    # Should be expired with 0 day TTL
    assert cache.is_expired("test123", 0) is True


def test_cache_nonexistent_expiration(tmp_path):
    """Test that nonexistent paper is considered expired."""
    cache = CacheManager(tmp_path / "test.db")
    assert cache.is_expired("nonexistent", 30) is True


def test_cache_complex_paper(tmp_path):
    """Test caching a paper with all fields populated."""
    cache = CacheManager(tmp_path / "test.db")
    paper = Paper(
        paper_id="complex123",
        title="Complex Paper",
        abstract="This is a complex paper with all fields",
        year=2024,
        authors=[Author(name="John Doe", author_id="author1")],
        venue="Conference 2024",
        citation_count=42,
        reference_count=100,
        url="https://example.com/paper"
    )
    
    cache.set("complex123", paper, "semantic_scholar")
    retrieved = cache.get("complex123")
    
    assert retrieved is not None
    assert retrieved.paper_id == "complex123"
    assert retrieved.title == "Complex Paper"
    assert retrieved.abstract == "This is a complex paper with all fields"
    assert retrieved.year == 2024
    assert len(retrieved.authors) == 1
    assert retrieved.authors[0].name == "John Doe"
    assert retrieved.venue == "Conference 2024"
    assert retrieved.citation_count == 42
    assert retrieved.reference_count == 100
    assert retrieved.url == "https://example.com/paper"


def test_cache_update(tmp_path):
    """Test that updating a cached paper replaces the old entry."""
    cache = CacheManager(tmp_path / "test.db")
    
    # Set initial paper
    paper1 = Paper(paper_id="update123", title="Original Title")
    cache.set("update123", paper1, "test")
    
    paper2 = Paper(paper_id="update123", title="Updated Title", year=2025)
    cache.set("update123", paper2, "test")
    
    # Retrieve and verify it's the updated version
    retrieved = cache.get("update123")
    assert retrieved is not None
    assert retrieved.title == "Updated Title"
    assert retrieved.year == 2025
