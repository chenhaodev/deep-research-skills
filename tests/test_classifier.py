from unittest.mock import AsyncMock, Mock

import pytest

from deep_research.api.models import Paper, QwenResponse
from deep_research.core.classifier import StudyClassifier


@pytest.mark.asyncio
async def test_classify_keywords_match():
    papers = [
        Paper(
            paper_id="P1",
            title="Randomized controlled trial of X",
            abstract="",
            citation_count=10
        ),
        Paper(
            paper_id="P2",
            title="A meta-analysis of Y",
            abstract="",
            citation_count=10
        ),
        Paper(
            paper_id="P3",
            title="Protocol",
            abstract="This is a literature review protocol",
            citation_count=10
        ),
        Paper(
            paper_id="P4",
            title="Observational cohort study",
            abstract="",
            citation_count=10
        )
    ]
    qwen_client = Mock()
    qwen_client.complete = AsyncMock()

    classifier = StudyClassifier()

    result = await classifier.classify_studies(papers, qwen_client)

    types = {item["paper"].paper_id: item["study_type"] for item in result}
    assert types["P1"] == "RCT"
    assert types["P2"] == "Meta-Analysis"
    assert types["P3"] == "Systematic Review"
    assert types["P4"] == "Observational"
    qwen_client.complete.assert_not_awaited()


@pytest.mark.asyncio
async def test_classify_uses_llm_fallback():
    paper = Paper(
        paper_id="P5",
        title="Ambiguous Study",
        abstract="No matching keywords here.",
        citation_count=20
    )
    qwen_client = Mock()
    qwen_client.complete = AsyncMock(return_value=QwenResponse(content="Observational", model="test"))

    classifier = StudyClassifier()

    result = await classifier.classify_studies([paper], qwen_client)

    assert result[0]["study_type"] == "Observational"
    qwen_client.complete.assert_awaited_once()
    assert "Classify the study type" in qwen_client.complete.call_args.args[0]


@pytest.mark.asyncio
async def test_badges_assigned_from_citations_and_journal_proxy():
    paper = Paper(
        paper_id="P6",
        title="Randomized controlled trial",
        abstract="",
        citation_count=150,
        reference_count=12000
    )
    qwen_client = Mock()
    qwen_client.complete = AsyncMock()

    classifier = StudyClassifier()

    result = await classifier.classify_studies([paper], qwen_client)

    badges = result[0]["badges"]
    assert "HIGHLY CITED" in badges
    assert "RIGOROUS JOURNAL" in badges
