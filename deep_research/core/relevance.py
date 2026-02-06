from typing import List

from sentence_transformers import SentenceTransformer, util

from deep_research.api.models import Paper


class RelevanceScorer:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    async def score_papers(
        self,
        query: str,
        papers: List[Paper],
        threshold: float = 0.6
    ) -> List[Paper]:
        if not papers:
            return []

        query_embedding = self.model.encode(query, convert_to_tensor=True)
        paper_texts = [self._paper_text(paper) for paper in papers]
        paper_embeddings = self.model.encode(paper_texts, convert_to_tensor=True)

        cosine_scores = util.cos_sim(query_embedding, paper_embeddings)[0]
        scored = []
        for paper, score in zip(papers, cosine_scores):
            scored.append((paper, float(score)))

        filtered = [item for item in scored if item[1] >= threshold]
        filtered.sort(key=lambda item: item[1], reverse=True)
        return [paper for paper, _ in filtered]

    def _paper_text(self, paper: Paper) -> str:
        if paper.has_abstract:
            return f"{paper.title} {paper.abstract}".strip()
        return paper.title
