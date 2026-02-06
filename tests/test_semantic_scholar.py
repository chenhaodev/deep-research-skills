import pytest
import httpx
import respx
from deep_research.api.semantic_scholar import SemanticScholarClient


@pytest.mark.asyncio
@respx.mock
async def test_search_papers_success():
    client = SemanticScholarClient()
    
    respx.get("https://api.semanticscholar.org/graph/v1/paper/search").mock(
        return_value=httpx.Response(200, json={
            "data": [
                {
                    "paperId": "test123",
                    "title": "Test Paper",
                    "abstract": "Test abstract",
                    "year": 2023,
                    "authors": [{"name": "Test Author"}],
                    "citationCount": 100
                }
            ],
            "total": 1
        })
    )
    
    result = await client.search_papers("machine learning", limit=10)
    assert len(result.papers) == 1
    assert result.papers[0].title == "Test Paper"
    assert result.total == 1


@pytest.mark.asyncio
@respx.mock
async def test_get_paper_not_found():
    client = SemanticScholarClient()
    
    respx.get("https://api.semanticscholar.org/graph/v1/paper/invalid_id").mock(
        return_value=httpx.Response(404, json={"error": "Paper not found"})
    )
    
    with pytest.raises(Exception, match="404|not found"):
        await client.get_paper("invalid_id")


@pytest.mark.asyncio
@respx.mock
async def test_get_citations():
    client = SemanticScholarClient()
    
    respx.get("https://api.semanticscholar.org/graph/v1/paper/test123/citations").mock(
        return_value=httpx.Response(200, json={
            "data": [
                {
                    "citingPaper": {
                        "paperId": "cite1",
                        "title": "Citing Paper",
                        "year": 2024
                    }
                }
            ]
        })
    )
    
    citations = await client.get_citations("test123", limit=10)
    assert len(citations) == 1
    assert citations[0].paper_id == "cite1"
