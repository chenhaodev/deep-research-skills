import asyncio
from datetime import datetime, timedelta, timezone
from typing import List, Optional

from deep_research.api.models import Paper
from deep_research.api.semantic_scholar import SemanticScholarClient
from deep_research.utils.logging import get_logger


logger = get_logger(__name__)


class CitationGraphExplorer:
    def __init__(self, semantic_client: Optional[SemanticScholarClient] = None):
        self.semantic_client = semantic_client or SemanticScholarClient()

    async def explore(self, seed_papers: List[Paper], max_depth: int = 2) -> List[Paper]:
        logger.info(f"CitationGraph: exploring with max_depth={max_depth}")

        visited = {paper.paper_id for paper in seed_papers}
        current_level = list(seed_papers)
        results: List[Paper] = []

        for depth in range(1, max_depth + 1):
            next_level: List[Paper] = []
            for paper in current_level:
                if not self._should_traverse(paper):
                    continue

                citations_task = asyncio.create_task(
                    self.semantic_client.get_citations(paper.paper_id)
                )
                references_task = asyncio.create_task(
                    self.semantic_client.get_references(paper.paper_id)
                )

                citations, references = await asyncio.gather(
                    citations_task,
                    references_task
                )

                for related in list(citations) + list(references):
                    if related.paper_id in visited:
                        continue
                    visited.add(related.paper_id)
                    results.append(related)
                    next_level.append(related)

            logger.info(f"CitationGraph: depth {depth} added {len(next_level)} papers")
            current_level = next_level

        return results

    def _should_traverse(self, paper: Paper) -> bool:
        if self._is_recent(paper):
            return True
        return paper.citation_count > 50

    def _is_recent(self, paper: Paper) -> bool:
        publication_date = self._parse_date(paper)
        if publication_date is None:
            return False
        now = datetime.now(timezone.utc)
        return now - publication_date <= timedelta(days=365)

    def _parse_date(self, paper: Paper) -> Optional[datetime]:
        if paper.publication_date:
            date_value = self._parse_iso_date(paper.publication_date)
            if date_value is not None:
                return date_value

        if paper.year:
            return datetime(paper.year, 1, 1, tzinfo=timezone.utc)

        return None

    def _parse_iso_date(self, value: str) -> Optional[datetime]:
        try:
            parsed = datetime.fromisoformat(value)
        except ValueError:
            parsed = None

        if parsed is None and len(value) == 4 and value.isdigit():
            parsed = datetime(int(value), 1, 1)

        if parsed is None:
            return None

        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)
        return parsed
