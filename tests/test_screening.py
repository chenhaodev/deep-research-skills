import sys
import types
from typing import Any, cast
from unittest.mock import AsyncMock, Mock

import pytest

from deep_research.api.models import Paper
from deep_research.config import SearchConfig


def _install_sentence_transformers_stub() -> None:
    if "sentence_transformers" in sys.modules:
        return

    stub = types.ModuleType("sentence_transformers")
    cast(Any, stub).SentenceTransformer = object
    cast(Any, stub).util = types.SimpleNamespace(cos_sim=lambda *args, **kwargs: [])
    sys.modules["sentence_transformers"] = stub


_install_sentence_transformers_stub()

import deep_research.core.screening as screening


@pytest.mark.asyncio
async def test_run_screening_funnel_order_and_logging(monkeypatch):
    call_order = []

    def deduplicate(papers):
        call_order.append("dedup")
        return papers[:2]

    def filter_by_quality(papers, config):
        call_order.append("quality")
        return papers[:1]

    async def score_papers(query, papers, threshold: float = 0.6):
        call_order.append("relevance")
        return papers

    dedup_engine = Mock()
    quality_checker = Mock()
    relevance_scorer = Mock()
    dedup_engine.deduplicate = Mock(side_effect=deduplicate)
    quality_checker.filter_by_quality = Mock(side_effect=filter_by_quality)
    relevance_scorer.score_papers = AsyncMock(side_effect=score_papers)

    logger = Mock()
    monkeypatch.setattr(screening, "logger", logger)

    pipeline = screening.ScreeningPipeline(
        dedup_engine=dedup_engine,
        quality_checker=quality_checker,
        relevance_scorer=relevance_scorer
    )

    papers = [
        Paper(paper_id="P1", title="Paper 1"),
        Paper(paper_id="P2", title="Paper 2"),
        Paper(paper_id="P3", title="Paper 3")
    ]
    config = SearchConfig(relevance_threshold=0.6)

    result = await pipeline.run_screening(papers, "test query", config)

    assert call_order == ["dedup", "quality", "relevance"]
    assert [paper.paper_id for paper in result] == ["P1"]
    quality_checker.filter_by_quality.assert_called_once_with(papers[:2], config)
    relevance_scorer.score_papers.assert_awaited_once_with(
        "test query",
        papers[:1],
        threshold=0.6
    )
    logger.info.assert_called_once_with(
        "Screening: 3 → 2 dedup → 1 quality → 1 relevant"
    )
