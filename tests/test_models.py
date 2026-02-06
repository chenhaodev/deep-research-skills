from deep_research.api.models import Author, Paper, ExternalIds, SearchResult


def test_paper_has_abstract():
    paper = Paper(paper_id="123", title="Test", abstract="This is a test abstract")
    assert paper.has_abstract is True
    
    paper_no_abstract = Paper(paper_id="456", title="Test2")
    assert paper_no_abstract.has_abstract is False


def test_paper_abstract_word_count():
    paper = Paper(paper_id="123", title="Test", abstract="This is a test abstract with seven words")
    assert paper.abstract_word_count == 8
    
    paper_no_abstract = Paper(paper_id="456", title="Test2")
    assert paper_no_abstract.abstract_word_count == 0


def test_search_result():
    papers = [
        Paper(paper_id="1", title="Paper 1"),
        Paper(paper_id="2", title="Paper 2")
    ]
    result = SearchResult(papers=papers, total=100, offset=0)
    assert len(result.papers) == 2
    assert result.total == 100
