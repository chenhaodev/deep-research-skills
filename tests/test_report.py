from deep_research.api.models import Author, ExternalIds, Paper
from deep_research.core.report import ReportGenerator


def test_report_markdown_structure_and_citations():
    papers = [
        Paper(
            paper_id="P1",
            title="Paper One",
            abstract="",
            year=2023,
            authors=[Author(name="Smith J")],
            venue="Nature",
            external_ids=ExternalIds(doi="10.1234/one")
        ),
        Paper(
            paper_id="P2",
            title="Paper Two",
            abstract="",
            year=2022,
            authors=[Author(name="Lee K"), Author(name="Patel M")],
            venue="Science",
            external_ids=ExternalIds(doi="10.1234/two")
        )
    ]
    evidence = [
        {"paper": papers[0], "claims": ["Claim A"], "strength": "STRONG"},
        {"paper": papers[1], "claims": ["Claim B"], "strength": "MODERATE"}
    ]
    consensus = {
        "question": "Does it work?",
        "yes_percent": 60.0,
        "no_percent": 20.0,
        "mixed_percent": 20.0,
        "possibly_percent": 0.0,
        "total_papers": 5,
        "confidence": 0.5
    }
    gaps = {
        "themes": ["Theme A", "Theme B", "Theme C", "Theme D", "Theme E"],
        "technologies": ["Tech 1", "Tech 2", "Tech 3", "Tech 4", "Tech 5"],
        "matrix": [
            [1, 0, 0, 0, 0],
            [0, 2, 0, 0, 0],
            [0, 0, 3, 0, 0],
            [0, 0, 0, 4, 0],
            [0, 0, 0, 0, 5]
        ],
        "gaps": [
            {"theme": "Theme A", "tech": "Tech 2", "opportunity": "Opp"}
        ]
    }

    report = ReportGenerator().generate_report(papers, evidence, consensus, gaps)

    assert "## Introduction" in report
    assert "## Methods" in report
    assert "## Results" in report
    assert "## Discussion" in report
    assert "## References" in report
    assert "Consensus Analysis" in report
    assert "Gap Analysis Matrix" in report
    assert "CONSENSUS METER" in report
    assert "[1]" in report
    assert "[2]" in report
    assert "[1] Smith J." in report
    assert "(2023). Paper One." in report
    assert "DOI: 10.1234/one" in report
