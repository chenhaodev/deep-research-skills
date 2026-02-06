from unittest.mock import AsyncMock, Mock

import pytest

from deep_research.api.models import Paper, SearchResult
from deep_research.core.search_orchestrator import SearchOrchestrator


@pytest.mark.asyncio
async def test_run_full_search_workflow_and_deduplication():
    survey_engine = Mock()
    strategy_generator = Mock()
    query_builder = Mock()
    citation_graph = Mock()

    call_order = []

    async def run_survey(query: str):
        call_order.append("survey")
        return SearchResult(
            papers=[Paper(paper_id="P1", title="Paper 1"), Paper(paper_id="P2", title="Paper 2")],
            total=2,
            offset=0
        )

    async def generate_strategy(query: str, survey_results):
        call_order.append("strategy")
        return {"bottlenecks": ["q1", "q2"]}

    async def execute_queries(strategies):
        call_order.append("query_builder")
        return [Paper(paper_id="P2", title="Paper 2"), Paper(paper_id="P3", title="Paper 3")]

    async def explore(seed_papers, max_depth: int = 2):
        call_order.append("citation_graph")
        return [Paper(paper_id="P3", title="Paper 3"), Paper(paper_id="P4", title="Paper 4")]

    survey_engine.run_survey = AsyncMock(side_effect=run_survey)
    strategy_generator.generate_strategy = AsyncMock(side_effect=generate_strategy)
    query_builder.execute_queries = AsyncMock(side_effect=execute_queries)
    citation_graph.explore = AsyncMock(side_effect=explore)

    orchestrator = SearchOrchestrator(
        survey_engine=survey_engine,
        strategy_generator=strategy_generator,
        query_builder=query_builder,
        citation_graph=citation_graph
    )

    result = await orchestrator.run_full_search("test query")

    assert call_order == ["survey", "strategy", "query_builder", "citation_graph"]
    assert result.total == 4
    assert {paper.paper_id for paper in result.papers} == {"P1", "P2", "P3", "P4"}
    citation_graph.explore.assert_called_once()
