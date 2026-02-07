import re
from typing import Dict, List, Optional

from deep_research.api.models import Paper
from deep_research.api.qwen import QwenClient
from deep_research.utils.logging import get_logger


logger = get_logger(__name__)

STRONG_CITATION_THRESHOLD = 100
JOURNAL_IMPACT_THRESHOLD = 10000

RCT_PHRASES = [
    "randomized controlled trial",
    "randomized trial",
    "random assignment"
]
META_PHRASES = [
    "meta-analysis",
    "systematic review and meta-analysis"
]
SYSTEMATIC_PHRASES = [
    "systematic review",
    "literature review"
]
OBSERVATIONAL_PHRASES = [
    "observational study",
    "cohort study",
    "case-control",
    "cross-sectional",
    "longitudinal study"
]


class StudyClassifier:
    async def classify_studies(
        self,
        papers: List[Paper],
        qwen_client: QwenClient
    ) -> List[Dict]:
        logger.info("Classifying studies...")
        results = []
        for paper in papers:
            study_type = self._classify_by_keywords(paper)
            if study_type is None:
                study_type = await self._classify_with_llm(paper, qwen_client)
            badges = self._assign_badges(paper)
            results.append({
                "paper": paper,
                "study_type": study_type,
                "badges": badges
            })
        return results

    def _classify_by_keywords(self, paper: Paper) -> Optional[str]:
        text = self._paper_text(paper)

        if self._contains_rct(text):
            return "RCT"
        if self._contains_any(text, META_PHRASES):
            return "Meta-Analysis"
        if self._is_systematic_review(text):
            return "Systematic Review"
        if self._contains_any(text, OBSERVATIONAL_PHRASES):
            return "Observational"
        return None

    def _contains_rct(self, text: str) -> bool:
        if self._contains_any(text, RCT_PHRASES):
            return True
        return re.search(r"\brct\b", text) is not None

    def _is_systematic_review(self, text: str) -> bool:
        if "systematic review" in text:
            return True
        return "literature review" in text and "protocol" in text

    def _contains_any(self, text: str, phrases: List[str]) -> bool:
        return any(phrase in text for phrase in phrases)

    async def _classify_with_llm(self, paper: Paper, qwen_client: QwenClient) -> str:
        abstract = paper.abstract or ""
        prompt = (
            "Classify the study type of the paper titled "
            f"'{paper.title}' with abstract '{abstract}'. Output EXACTLY one of: "
            "RCT, Meta-Analysis, Systematic Review, Observational, Case Study, Opinion, Other."
        )
        response = await qwen_client.complete(prompt)
        return self._normalize_llm_choice(response.content)

    def _normalize_llm_choice(self, content: str) -> str:
        choices = {
            "RCT": "RCT",
            "META-ANALYSIS": "Meta-Analysis",
            "SYSTEMATIC REVIEW": "Systematic Review",
            "OBSERVATIONAL": "Observational",
            "CASE STUDY": "Case Study",
            "OPINION": "Opinion",
            "OTHER": "Other"
        }
        tokens = re.findall(r"[A-Z]+(?:-[A-Z]+)?", content.upper())
        for token in tokens:
            if token in choices:
                return choices[token]
        for key, value in choices.items():
            if key in content.upper():
                return value
        return "Other"

    def _assign_badges(self, paper: Paper) -> List[str]:
        badges = []
        if paper.reference_count > JOURNAL_IMPACT_THRESHOLD:
            badges.append("RIGOROUS JOURNAL")
        if paper.citation_count > STRONG_CITATION_THRESHOLD:
            badges.append("HIGHLY CITED")
        return badges

    def _paper_text(self, paper: Paper) -> str:
        abstract = paper.abstract or ""
        return f"{paper.title} {abstract}".lower()
