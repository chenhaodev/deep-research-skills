from typing import List, Optional

from deep_research.api.models import Paper, SearchResult
from deep_research.core.citation_graph import CitationGraphExplorer
from deep_research.core.query_builder import QueryBuilder
from deep_research.core.strategy import StrategyGenerator
from deep_research.core.survey import SurveyEngine
from deep_research.utils.logging import get_logger


logger = get_logger(__name__)


class SearchOrchestrator:
    def __init__(
        self,
        survey_engine: Optional[SurveyEngine] = None,
        strategy_generator: Optional[StrategyGenerator] = None,
        query_builder: Optional[QueryBuilder] = None,
        citation_graph: Optional[CitationGraphExplorer] = None
    ):
        self.survey_engine = survey_engine or SurveyEngine()
        self.strategy_generator = strategy_generator or StrategyGenerator()
        self.query_builder = query_builder or QueryBuilder()
        self.citation_graph = citation_graph or CitationGraphExplorer()

    async def run_full_search(self, query: str) -> SearchResult:
        logger.info("SearchOrchestrator: starting survey")
        survey_result = await self.survey_engine.run_survey(query)

        logger.info("SearchOrchestrator: generating strategy")
        strategies = await self.strategy_generator.generate_strategy(
            query,
            survey_result.papers
        )

        logger.info("SearchOrchestrator: executing multi-angle queries")
        query_results = await self.query_builder.execute_queries(strategies)

        seed_papers = self._dedupe_papers(survey_result.papers + query_results)
        logger.info("SearchOrchestrator: exploring citation graph")
        citation_results = await self.citation_graph.explore(seed_papers, max_depth=2)

        combined = self._dedupe_papers(seed_papers + citation_results)
        logger.info(f"SearchOrchestrator: returning {len(combined)} papers")
        return SearchResult(papers=combined, total=len(combined), offset=0)

    def _dedupe_papers(self, papers: List[Paper]) -> List[Paper]:
        seen = set()
        deduped = []
        for paper in papers:
            if paper.paper_id in seen:
                continue
            seen.add(paper.paper_id)
            deduped.append(paper)
        return deduped
