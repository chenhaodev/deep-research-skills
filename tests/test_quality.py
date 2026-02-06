from datetime import datetime

from deep_research.api.models import Paper
from deep_research.config import SearchConfig
from deep_research.core.quality import QualityChecker


def _make_abstract(word_count: int) -> str:
    return "word " * word_count


def test_quality_rejects_missing_abstract():
    current_year = datetime.now().year
    papers = [
        Paper(paper_id="P1", title="No Abstract", abstract=None, year=current_year)
    ]

    result = QualityChecker().filter_by_quality(papers, SearchConfig())

    assert result == []


def test_quality_rejects_short_abstract():
    current_year = datetime.now().year
    papers = [
        Paper(
            paper_id="P2",
            title="Short Abstract",
            abstract=_make_abstract(10),
            year=current_year
        )
    ]

    result = QualityChecker().filter_by_quality(papers, SearchConfig())

    assert result == []


def test_quality_rejects_out_of_range_date():
    current_year = datetime.now().year
    papers = [
        Paper(
            paper_id="P3",
            title="Old Paper",
            abstract=_make_abstract(60),
            year=current_year - 10
        )
    ]

    result = QualityChecker().filter_by_quality(papers, SearchConfig(date_range_years=3))

    assert result == []


def test_quality_allows_valid_paper():
    current_year = datetime.now().year
    papers = [
        Paper(
            paper_id="P4",
            title="Valid Paper",
            abstract=_make_abstract(60),
            year=current_year
        )
    ]

    result = QualityChecker().filter_by_quality(papers, SearchConfig())

    assert [paper.paper_id for paper in result] == ["P4"]
