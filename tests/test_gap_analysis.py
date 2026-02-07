from unittest.mock import AsyncMock, Mock

import pytest

from deep_research.api.models import Paper, QwenResponse
from deep_research.core.gap_analysis import GapAnalyzer


@pytest.mark.asyncio
async def test_gap_analysis_matrix_and_gaps_identified():
    papers = [
        Paper(
            paper_id="P1",
            title="Study 1",
            abstract="Theme A uses Tech 1 for results."
        ),
        Paper(
            paper_id="P2",
            title="Study 2",
            abstract="Theme B with Tech 2 applied."
        ),
        Paper(
            paper_id="P3",
            title="Study 3",
            abstract="Theme A and Tech 2 are combined."
        )
    ]

    qwen_client = Mock()
    qwen_client.complete = AsyncMock(side_effect=[
        QwenResponse(
            content='["Theme A", "Theme B", "Theme C", "Theme D", "Theme E"]',
            model="test"
        ),
        QwenResponse(
            content='["Tech 1", "Tech 2", "Tech 3", "Tech 4", "Tech 5"]',
            model="test"
        ),
        QwenResponse(
            content='["Opportunity 1", "Opportunity 2", "Opportunity 3"]',
            model="test"
        )
    ])

    analyzer = GapAnalyzer()

    result = await analyzer.analyze_gaps(papers, qwen_client)

    assert result["themes"][:2] == ["Theme A", "Theme B"]
    assert result["technologies"][:2] == ["Tech 1", "Tech 2"]
    matrix = result["matrix"]
    assert len(matrix) == 5
    assert all(len(row) == 5 for row in matrix)
    assert matrix[0][0] == 1
    assert matrix[0][1] == 1
    assert matrix[1][1] == 1
    assert any(
        gap["theme"] == "Theme C" and gap["tech"] == "Tech 1"
        for gap in result["gaps"]
    )
    assert all(gap["opportunity"] for gap in result["gaps"])
    qwen_client.complete.assert_awaited()
