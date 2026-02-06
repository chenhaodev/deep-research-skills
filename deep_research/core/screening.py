from typing import List, Optional

from deep_research.api.models import Paper
from deep_research.config import SearchConfig
from deep_research.core.deduplication import DeduplicationEngine
from deep_research.core.quality import QualityChecker
from deep_research.core.relevance import RelevanceScorer
from deep_research.utils.logging import get_logger


logger = get_logger(__name__)


class ScreeningPipeline:
    def __init__(
        self,
        dedup_engine: Optional[DeduplicationEngine] = None,
        quality_checker: Optional[QualityChecker] = None,
        relevance_scorer: Optional[RelevanceScorer] = None
    ):
        self.dedup_engine = dedup_engine or DeduplicationEngine()
        self.quality_checker = quality_checker or QualityChecker()
        self.relevance_scorer = relevance_scorer or RelevanceScorer()

    async def run_screening(
        self,
        papers: List[Paper],
        query: str,
        config: SearchConfig
    ) -> List[Paper]:
        initial = len(papers)

        deduped = self.dedup_engine.deduplicate(papers)
        after_dedup = len(deduped)

        quality_filtered = self.quality_checker.filter_by_quality(deduped, config)
        after_quality = len(quality_filtered)

        relevant = await self.relevance_scorer.score_papers(
            query,
            quality_filtered,
            threshold=config.relevance_threshold
        )
        final = len(relevant)

        logger.info(
            f"Screening: {initial} → {after_dedup} dedup → "
            f"{after_quality} quality → {final} relevant"
        )
        return relevant
