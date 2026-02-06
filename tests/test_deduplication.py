from deep_research.api.models import ExternalIds, Paper
from deep_research.core.deduplication import DeduplicationEngine


def test_deduplicate_by_external_ids_keeps_first():
    papers = [
        Paper(
            paper_id="P1",
            title="Paper One",
            external_ids=ExternalIds(doi="10.1/abc", pmid="111", s2_id="s2-1")
        ),
        Paper(
            paper_id="P2",
            title="Paper Two",
            external_ids=ExternalIds(doi="10.1/abc", pmid="222", s2_id="s2-2")
        ),
        Paper(
            paper_id="P3",
            title="Paper Three",
            external_ids=ExternalIds(pmid="111", s2_id="s2-3")
        ),
        Paper(
            paper_id="P4",
            title="Paper Four",
            external_ids=ExternalIds(s2_id="s2-1")
        ),
        Paper(
            paper_id="P5",
            title="Paper Five",
            external_ids=ExternalIds(doi="10.2/xyz")
        )
    ]

    result = DeduplicationEngine().deduplicate(papers)

    assert [paper.paper_id for paper in result] == ["P1", "P5"]


def test_deduplicate_by_title_similarity():
    papers = [
        Paper(paper_id="P1", title="Deep Learning: A Survey"),
        Paper(paper_id="P2", title="deep learning a survey"),
        Paper(paper_id="P3", title="Deep Learning in Medicine")
    ]

    result = DeduplicationEngine().deduplicate(papers)

    assert [paper.paper_id for paper in result] == ["P1", "P3"]
