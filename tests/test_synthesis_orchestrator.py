from unittest.mock import AsyncMock, Mock

import pytest

from deep_research.api.models import Paper
from deep_research.core.synthesis_orchestrator import SynthesisOrchestrator


@pytest.mark.asyncio
async def test_synthesize_runs_full_workflow_for_binary_question():
    papers = [Paper(paper_id="P1", title="Paper 1")]
    qwen_client = Mock()

    evidence_extractor = Mock()
    evidence_extractor.extract_evidence = AsyncMock(return_value=[
        {"paper": papers[0], "claims": ["Claim"], "strength": "STRONG"}
    ])
    classifier = Mock()
    classifier.classify_studies = AsyncMock(return_value=[
        {"paper": papers[0], "study_type": "RCT", "badges": []}
    ])
    consensus_analyzer = Mock()
    consensus_analyzer.quantify_consensus = AsyncMock(return_value={
        "question": "Does it work?",
        "yes_percent": 100.0,
        "no_percent": 0.0,
        "mixed_percent": 0.0,
        "possibly_percent": 0.0,
        "total_papers": 5,
        "confidence": 0.5
    })
    gap_analyzer = Mock()
    gap_analyzer.analyze_gaps = AsyncMock(return_value={
        "themes": [],
        "technologies": [],
        "matrix": [],
        "gaps": []
    })
    report_generator = Mock()
    report_generator.generate_report = Mock(return_value="REPORT")

    orchestrator = SynthesisOrchestrator(
        evidence_extractor=evidence_extractor,
        classifier=classifier,
        consensus_analyzer=consensus_analyzer,
        gap_analyzer=gap_analyzer,
        report_generator=report_generator
    )

    result = await orchestrator.synthesize(papers, "Does it work?", qwen_client)

    evidence_extractor.extract_evidence.assert_awaited_once_with(papers, qwen_client)
    classifier.classify_studies.assert_awaited_once_with(papers, qwen_client)
    consensus_analyzer.quantify_consensus.assert_awaited_once_with(
        papers,
        "Does it work?",
        qwen_client
    )
    gap_analyzer.analyze_gaps.assert_awaited_once_with(papers, qwen_client)
    report_generator.generate_report.assert_called_once()
    assert result["report"] == "REPORT"


@pytest.mark.asyncio
async def test_synthesize_skips_consensus_for_non_binary_query():
    papers = [Paper(paper_id="P2", title="Paper 2")]
    qwen_client = Mock()

    evidence_extractor = Mock()
    evidence_extractor.extract_evidence = AsyncMock(return_value=[])
    classifier = Mock()
    classifier.classify_studies = AsyncMock(return_value=[])
    consensus_analyzer = Mock()
    consensus_analyzer.quantify_consensus = AsyncMock()
    gap_analyzer = Mock()
    gap_analyzer.analyze_gaps = AsyncMock(return_value={
        "themes": [],
        "technologies": [],
        "matrix": [],
        "gaps": []
    })
    report_generator = Mock()
    report_generator.generate_report = Mock(return_value="REPORT")

    orchestrator = SynthesisOrchestrator(
        evidence_extractor=evidence_extractor,
        classifier=classifier,
        consensus_analyzer=consensus_analyzer,
        gap_analyzer=gap_analyzer,
        report_generator=report_generator
    )

    result = await orchestrator.synthesize(papers, "Explain why it works", qwen_client)

    consensus_analyzer.quantify_consensus.assert_not_called()
    assert result["consensus"] == {}
