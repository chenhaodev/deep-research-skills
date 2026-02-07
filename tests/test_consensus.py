from unittest.mock import Mock

import pytest

from deep_research.api.models import Paper, QwenResponse
from deep_research.core.consensus import ConsensusAnalyzer


def _make_papers(count: int):
    return [
        Paper(paper_id=f"P{i}", title=f"Paper {i}", abstract=f"Abstract {i}")
        for i in range(1, count + 1)
    ]


@pytest.mark.asyncio
async def test_quantify_consensus_percentages_and_confidence():
    papers = _make_papers(5)
    question = "Does it work?"

    filter_answers = {
        "Paper 1": "YES",
        "Paper 2": "YES",
        "Paper 3": "YES",
        "Paper 4": "YES",
        "Paper 5": "YES"
    }
    stance_answers = {
        "Paper 1": "YES",
        "Paper 2": "NO",
        "Paper 3": "MIXED",
        "Paper 4": "POSSIBLY",
        "Paper 5": "YES"
    }

    async def complete(prompt: str, max_tokens: int = 4096, temperature: float = 0.7):
        if prompt.startswith("Does the paper"):
            for title, answer in filter_answers.items():
                if title in prompt:
                    return QwenResponse(content=answer, model="test")
        if prompt.startswith("What is this paper's answer"):
            for title, answer in stance_answers.items():
                if title in prompt:
                    return QwenResponse(content=answer, model="test")
        return QwenResponse(content="NO", model="test")

    qwen_client = Mock()
    qwen_client.complete = complete

    analyzer = ConsensusAnalyzer()

    result = await analyzer.quantify_consensus(papers, question, qwen_client)

    assert result["total_papers"] == 5
    assert result["yes_percent"] == pytest.approx(40.0)
    assert result["no_percent"] == pytest.approx(20.0)
    assert result["mixed_percent"] == pytest.approx(20.0)
    assert result["possibly_percent"] == pytest.approx(20.0)
    assert result["confidence"] == pytest.approx(0.5)


@pytest.mark.asyncio
async def test_quantify_consensus_raises_when_insufficient_data():
    papers = _make_papers(4)
    question = "Does it work?"

    async def complete(prompt: str, max_tokens: int = 4096, temperature: float = 0.7):
        return QwenResponse(content="YES", model="test")

    qwen_client = Mock()
    qwen_client.complete = complete

    analyzer = ConsensusAnalyzer()

    with pytest.raises(ValueError, match="INSUFFICIENT DATA"):
        await analyzer.quantify_consensus(papers, question, qwen_client)
