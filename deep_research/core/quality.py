from datetime import datetime
from typing import List

from deep_research.api.models import Paper
from deep_research.config import SearchConfig


class QualityChecker:
    def filter_by_quality(self, papers: List[Paper], config: SearchConfig) -> List[Paper]:
        min_year = datetime.now().year - config.date_range_years
        filtered = []

        for paper in papers:
            if not paper.has_abstract:
                continue
            if paper.abstract_word_count < config.min_abstract_words:
                continue
            if paper.year is None:
                continue
            if paper.year < min_year:
                continue
            filtered.append(paper)

        return filtered
