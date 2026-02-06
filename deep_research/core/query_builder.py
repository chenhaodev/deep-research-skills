import asyncio
from typing import Dict, List, Optional

from deep_research.api.models import Paper, SearchResult
from deep_research.api.pubmed import PubMedClient
from deep_research.api.semantic_scholar import SemanticScholarClient
from deep_research.utils.fetcher import fetch_parallel
from deep_research.utils.logging import get_logger


logger = get_logger(__name__)


class QueryBuilder:
    def __init__(
        self,
        semantic_client: Optional[SemanticScholarClient] = None,
        pubmed_client: Optional[PubMedClient] = None
    ):
        self.semantic_client = semantic_client or SemanticScholarClient()
        self.pubmed_client = pubmed_client or PubMedClient()

    async def execute_queries(self, strategies: Dict[str, List[str]]) -> List[Paper]:
        queries = [query for queries in strategies.values() for query in queries]
        logger.info(f"QueryBuilder: executing {len(queries)} queries")

        results = await fetch_parallel(queries, self._execute_query, max_concurrent=5)

        papers: List[Paper] = []
        for result in results:
            if isinstance(result, Exception):
                logger.warning(f"QueryBuilder: query failed with {result}")
                continue
            papers.extend(result)

        return self._dedupe_papers(papers)

    async def _execute_query(self, query: str) -> List[Paper]:
        semantic_task = asyncio.create_task(
            self.semantic_client.search_papers(query, limit=10)
        )
        pubmed_task = asyncio.create_task(self._search_pubmed(query))

        semantic_result, pubmed_papers = await asyncio.gather(semantic_task, pubmed_task)
        papers = list(semantic_result.papers) + list(pubmed_papers)
        return papers

    async def _search_pubmed(self, query: str) -> List[Paper]:
        pmids = await self.pubmed_client.search(query, max_results=10)
        return await self.pubmed_client.fetch_details(pmids)

    def _dedupe_papers(self, papers: List[Paper]) -> List[Paper]:
        seen = set()
        deduped = []
        for paper in papers:
            if paper.paper_id in seen:
                continue
            seen.add(paper.paper_id)
            deduped.append(paper)
        return deduped
