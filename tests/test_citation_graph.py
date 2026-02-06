from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock, Mock

import pytest

from deep_research.api.models import Paper
from deep_research.core.citation_graph import CitationGraphExplorer


@pytest.mark.asyncio
async def test_explore_two_levels_and_threshold():
    semantic_client = Mock()

    recent_date = (datetime.now(timezone.utc) - timedelta(days=180)).date().isoformat()

    seed_eligible = Paper(
        paper_id="seed1",
        title="Seed Eligible",
        citation_count=60,
        publication_date="2018-01-01"
    )
    seed_ineligible = Paper(
        paper_id="seed2",
        title="Seed Ineligible",
        citation_count=10,
        publication_date="2010-01-01"
    )

    citations_map = {
        "seed1": [Paper(paper_id="c1", title="Citation 1", publication_date=recent_date)],
        "c1": [Paper(paper_id="c2", title="Citation 2", publication_date=recent_date)]
    }
    references_map = {
        "seed1": [Paper(paper_id="r1", title="Reference 1", publication_date=recent_date)],
        "r1": [Paper(paper_id="r2", title="Reference 2", publication_date=recent_date)]
    }

    async def get_citations(paper_id: str, limit: int = 100):
        return citations_map.get(paper_id, [])

    async def get_references(paper_id: str, limit: int = 100):
        return references_map.get(paper_id, [])

    semantic_client.get_citations = AsyncMock(side_effect=get_citations)
    semantic_client.get_references = AsyncMock(side_effect=get_references)

    explorer = CitationGraphExplorer(semantic_client=semantic_client)
    results = await explorer.explore([seed_eligible, seed_ineligible], max_depth=2)

    result_ids = {paper.paper_id for paper in results}
    assert result_ids == {"c1", "c2", "r1", "r2"}

    citation_calls = [call.args[0] for call in semantic_client.get_citations.call_args_list]
    reference_calls = [call.args[0] for call in semantic_client.get_references.call_args_list]

    assert "seed1" in citation_calls
    assert "seed1" in reference_calls
    assert "seed2" not in citation_calls
    assert "seed2" not in reference_calls
