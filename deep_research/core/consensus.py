import re
from typing import Dict, List, Optional

from deep_research.api.models import Paper
from deep_research.api.qwen import QwenClient
from deep_research.utils.logging import get_logger


logger = get_logger(__name__)

CONSENSUS_MIN_PAPERS = 5
CONSENSUS_FULL_CONFIDENCE = 10


class ConsensusAnalyzer:
    async def quantify_consensus(
        self,
        papers: List[Paper],
        question: str,
        qwen_client: QwenClient
    ) -> Dict:
        logger.info("Quantifying consensus...")
        relevant = []
        for paper in papers:
            prompt = (
                "Does the paper '[title]' with abstract '[abstract]' provide an answer "
                "or evidence regarding the question: '[question]'? Answer YES or NO."
            )
            prompt = prompt.replace("[title]", paper.title)
            prompt = prompt.replace("[abstract]", paper.abstract or "")
            prompt = prompt.replace("[question]", question)
            response = await qwen_client.complete(prompt)
            answer = self._normalize_binary(response.content)
            if answer == "YES":
                relevant.append(paper)

        counts = {"YES": 0, "NO": 0, "MIXED": 0, "POSSIBLY": 0}
        for paper in relevant:
            prompt = (
                "What is this paper's answer to the question: '[question]'? "
                "Based on the abstract, choose exactly one: YES, NO, MIXED, POSSIBLY. "
                "Title: [title]. Abstract: [abstract]."
            )
            prompt = prompt.replace("[question]", question)
            prompt = prompt.replace("[title]", paper.title)
            prompt = prompt.replace("[abstract]", paper.abstract or "")
            response = await qwen_client.complete(prompt)
            stance = self._normalize_choice(response.content, list(counts.keys()))
            counts[stance or "POSSIBLY"] += 1

        total = sum(counts.values())
        if total < CONSENSUS_MIN_PAPERS:
            raise ValueError("INSUFFICIENT DATA")

        yes_percent = counts["YES"] / total * 100
        no_percent = counts["NO"] / total * 100
        mixed_percent = counts["MIXED"] / total * 100
        possibly_percent = counts["POSSIBLY"] / total * 100
        confidence = min(1.0, total / CONSENSUS_FULL_CONFIDENCE)

        return {
            "question": question,
            "yes_percent": yes_percent,
            "no_percent": no_percent,
            "mixed_percent": mixed_percent,
            "possibly_percent": possibly_percent,
            "total_papers": total,
            "confidence": confidence
        }

    def _normalize_binary(self, content: str) -> str:
        tokens = re.findall(r"[A-Z]+", content.upper())
        if "YES" in tokens:
            return "YES"
        if "NO" in tokens:
            return "NO"
        return "NO"

    def _normalize_choice(self, content: str, choices: List[str]) -> Optional[str]:
        tokens = re.findall(r"[A-Z]+", content.upper())
        for token in tokens:
            if token in choices:
                return token
        upper = content.upper()
        for choice in choices:
            if choice in upper:
                return choice
        return None
