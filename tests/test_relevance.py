import sys
import types
from typing import Any, cast

import pytest

from deep_research.api.models import Paper


def _install_sentence_transformers_stub() -> None:
    if "sentence_transformers" in sys.modules:
        return

    stub = types.ModuleType("sentence_transformers")
    cast(Any, stub).SentenceTransformer = object
    cast(Any, stub).util = types.SimpleNamespace(cos_sim=lambda *args, **kwargs: [])
    sys.modules["sentence_transformers"] = stub


_install_sentence_transformers_stub()

import deep_research.core.relevance as relevance


class DummyModel:
    def __init__(self):
        self.encode_calls = []

    def encode(self, texts, convert_to_tensor: bool = True):
        self.encode_calls.append(texts)
        return texts


@pytest.mark.asyncio
async def test_score_papers_filters_and_sorts(monkeypatch):
    dummy_model = DummyModel()

    def fake_transformer(*args, **kwargs):
        return dummy_model

    def fake_cos_sim(query_embedding, paper_embeddings):
        return [[0.2, 0.75, 0.65]]

    monkeypatch.setattr(relevance, "SentenceTransformer", fake_transformer)
    monkeypatch.setattr(relevance.util, "cos_sim", fake_cos_sim)

    papers = [
        Paper(paper_id="P1", title="Alpha", abstract="A1"),
        Paper(paper_id="P2", title="Beta"),
        Paper(paper_id="P3", title="Gamma", abstract="G")
    ]

    scorer = relevance.RelevanceScorer()
    result = await scorer.score_papers("test query", papers, threshold=0.6)

    assert [paper.paper_id for paper in result] == ["P2", "P3"]
    assert dummy_model.encode_calls[0] == "test query"
    assert dummy_model.encode_calls[1] == ["Alpha A1", "Beta", "Gamma G"]
