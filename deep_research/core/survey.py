import asyncio
from typing import List, Optional

from deep_research.api.models import Paper, SearchResult
from deep_research.api.semantic_scholar import SemanticScholarClient
from deep_research.api.pubmed import PubMedClient
from deep_research.utils.logging import get_logger


logger = get_logger(__name__)


class SurveyEngine:
    def __init__(
        self,
        semantic_client: Optional[SemanticScholarClient] = None,
        pubmed_client: Optional[PubMedClient] = None
    ):
        self.semantic_client = semantic_client or SemanticScholarClient()
        self.pubmed_client = pubmed_client or PubMedClient()

    async def _search_semantic(self, query: str) -> SearchResult:
        logger.info("Survey: searching Semantic Scholar")
        return await self.semantic_client.search_papers(query, limit=100)

    async def _search_pubmed(self, query: str) -> List[Paper]:
        logger.info("Survey: searching PubMed")
        pmids = await self.pubmed_client.search(query, max_results=100)
        return await self.pubmed_client.fetch_details(pmids)

    async def run_survey(self, query: str) -> SearchResult:
        semantic_task = asyncio.create_task(self._search_semantic(query))
        pubmed_task = asyncio.create_task(self._search_pubmed(query))

        semantic_result, pubmed_papers = await asyncio.gather(
            semantic_task,
            pubmed_task
        )

        combined = list(semantic_result.papers) + list(pubmed_papers)
        combined.sort(key=lambda paper: paper.citation_count, reverse=True)
        top_papers = combined[:50]

        logger.info(f"Survey: returning {len(top_papers)} papers")
        return SearchResult(papers=top_papers, total=len(top_papers), offset=0)
