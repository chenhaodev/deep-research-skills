from unittest.mock import AsyncMock, Mock

import pytest

from deep_research.api.models import Paper, SearchResult
from deep_research.core.query_builder import QueryBuilder


@pytest.mark.asyncio
async def test_execute_queries_runs_all_and_deduplicates():
    semantic_client = Mock()
    pubmed_client = Mock()

    strategies = {
        "bottlenecks": ["query one", "query two"],
        "whitespace": ["query three"]
    }

    semantic_client.search_papers = AsyncMock(side_effect=[
        SearchResult(
            papers=[
                Paper(paper_id="S1", title="Semantic 1"),
                Paper(paper_id="DUP", title="Duplicate")
            ],
            total=2,
            offset=0
        ),
        SearchResult(
            papers=[
                Paper(paper_id="S2", title="Semantic 2"),
                Paper(paper_id="DUP", title="Duplicate")
            ],
            total=2,
            offset=0
        ),
        SearchResult(
            papers=[Paper(paper_id="S3", title="Semantic 3")],
            total=1,
            offset=0
        )
    ])

    pubmed_client.search = AsyncMock(side_effect=[
        ["1", "2"],
        ["3"],
        ["4"]
    ])
    pubmed_client.fetch_details = AsyncMock(side_effect=[
        [
            Paper(paper_id="P1", title="PubMed 1"),
            Paper(paper_id="DUP", title="Duplicate")
        ],
        [Paper(paper_id="P2", title="PubMed 2")],
        [Paper(paper_id="P3", title="PubMed 3")]
    ])

    builder = QueryBuilder(semantic_client=semantic_client, pubmed_client=pubmed_client)
    results = await builder.execute_queries(strategies)

    paper_ids = {paper.paper_id for paper in results}
    assert "DUP" in paper_ids
    assert len(paper_ids) == len(results)
    assert semantic_client.search_papers.call_count == 3
    assert pubmed_client.search.call_count == 3
    assert pubmed_client.fetch_details.call_count == 3
