from unittest.mock import AsyncMock, Mock

import pytest

from deep_research.api.models import Paper, QwenResponse
from deep_research.core.strategy import StrategyGenerator


@pytest.mark.asyncio
async def test_generate_strategy_six_angles_and_query_counts():
    qwen_client = Mock()
    qwen_client.complete = AsyncMock(
        return_value=QwenResponse(
            content='["neural networks", "deep learning", "representation learning"]',
            model="test-model",
            usage={}
        )
    )

    survey_results = [
        Paper(
            paper_id="S1",
            title="Survey Paper",
            abstract="This work studies neural networks and deep learning systems.",
            citation_count=120
        )
    ]

    generator = StrategyGenerator(qwen_client=qwen_client)
    strategy = await generator.generate_strategy("machine learning", survey_results)

    assert set(strategy.keys()) == {
        "bottlenecks",
        "whitespace",
        "scenarios",
        "terminology",
        "international",
        "foundational"
    }

    total_queries = 0
    for angle, queries in strategy.items():
        assert 3 <= len(queries) <= 4
        total_queries += len(queries)

        if angle == "bottlenecks":
            assert all("limitation" in query for query in queries)
        if angle == "whitespace":
            assert all("gap" in query for query in queries)
        if angle == "scenarios":
            assert all("application" in query for query in queries)
        if angle == "international":
            assert all("country" in query for query in queries)
        if angle == "foundational":
            assert all("review" in query for query in queries)

    assert total_queries <= 25
    assert any("neural networks" in query for query in strategy["terminology"])
    qwen_client.complete.assert_called_once()
