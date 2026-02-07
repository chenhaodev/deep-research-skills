from unittest.mock import AsyncMock, Mock

import pytest

from deep_research.api.models import Paper, QwenResponse
from deep_research.core.evidence import EvidenceExtractor
from deep_research.core.classifier import StudyClassifier


class StubClassifier(StudyClassifier):
    def __init__(self, mapping):
        self.mapping = mapping

    async def classify_studies(self, papers, qwen_client):
        return [
            {"paper": paper, "study_type": self.mapping.get(paper.paper_id, "Other"), "badges": []}
            for paper in papers
        ]


@pytest.mark.asyncio
async def test_extract_evidence_strength_and_filtering():
    papers = [
        Paper(paper_id="P1", title="RCT Study", abstract="A", citation_count=120),
        Paper(paper_id="P2", title="Moderate RCT", abstract="B", citation_count=60),
        Paper(paper_id="P3", title="Low Cited", abstract="C", citation_count=10),
        Paper(paper_id="P4", title="Case Study", abstract="D", citation_count=200)
    ]
    classifier = StubClassifier({
        "P1": "RCT",
        "P2": "RCT",
        "P3": "RCT",
        "P4": "Case Study"
    })
    qwen_client = Mock()
    qwen_client.complete = AsyncMock(side_effect=[
        QwenResponse(content='["claim 1"]', model="test"),
        QwenResponse(content='["claim 2"]', model="test"),
        QwenResponse(content='["claim 3"]', model="test"),
        QwenResponse(content='["claim 4"]', model="test")
    ])

    extractor = EvidenceExtractor(classifier=classifier)

    result = await extractor.extract_evidence(papers, qwen_client)

    assert [item["paper"].paper_id for item in result] == ["P1", "P2"]
    strengths = {item["paper"].paper_id: item["strength"] for item in result}
    assert strengths["P1"] == "STRONG"
    assert strengths["P2"] == "MODERATE"
    assert result[0]["claims"] == ["claim 1"]
    assert qwen_client.complete.await_count == 4
    assert qwen_client.complete.call_args_list[0].args[0] == (
        "Extract 1-3 key findings from this paper. Title: RCT Study. Abstract: A. Return as JSON array."
    )
