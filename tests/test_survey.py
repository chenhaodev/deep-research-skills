import asyncio
from unittest.mock import AsyncMock, Mock

import pytest

from deep_research.api.models import Paper, SearchResult
from deep_research.core.survey import SurveyEngine


@pytest.mark.asyncio
async def test_run_survey_parallel_and_top_50():
    semantic_client = Mock()
    pubmed_client = Mock()

    proceed = asyncio.Event()
    semantic_started = asyncio.Event()
    pubmed_started = asyncio.Event()

    semantic_papers = [
        Paper(paper_id=f"S{i}", title=f"Semantic {i}", citation_count=100 - i)
        for i in range(30)
    ]
    pubmed_papers = [
        Paper(paper_id=f"P{i}", title=f"PubMed {i}", citation_count=70 - i)
        for i in range(30)
    ]

    async def semantic_search(query: str, limit: int = 100, offset: int = 0, fields=None):
        semantic_started.set()
        await proceed.wait()
        return SearchResult(papers=semantic_papers, total=len(semantic_papers), offset=0)

    async def pubmed_search(query: str, max_results: int = 100):
        pubmed_started.set()
        await proceed.wait()
        return [str(i) for i in range(len(pubmed_papers))]

    async def pubmed_fetch_details(pmids):
        return pubmed_papers

    semantic_client.search_papers = AsyncMock(side_effect=semantic_search)
    pubmed_client.search = AsyncMock(side_effect=pubmed_search)
    pubmed_client.fetch_details = AsyncMock(side_effect=pubmed_fetch_details)

    engine = SurveyEngine(semantic_client=semantic_client, pubmed_client=pubmed_client)

    task = asyncio.create_task(engine.run_survey("test query"))
    await asyncio.wait_for(
        asyncio.gather(semantic_started.wait(), pubmed_started.wait()),
        timeout=1.0
    )
    proceed.set()

    result = await asyncio.wait_for(task, timeout=1.0)

    assert len(result.papers) == 50
    citation_counts = [paper.citation_count for paper in result.papers]
    assert citation_counts == sorted(citation_counts, reverse=True)
    semantic_client.search_papers.assert_called_once()
    pubmed_client.search.assert_called_once()
    pubmed_client.fetch_details.assert_called_once()
