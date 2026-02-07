import json
from typing import Dict, List, Optional

from deep_research.api.models import Paper
from deep_research.api.qwen import QwenClient
from deep_research.core.classifier import StudyClassifier
from deep_research.utils.logging import get_logger


logger = get_logger(__name__)

STRONG_CITATION_THRESHOLD = 100
MODERATE_CITATION_THRESHOLD = 50
MAX_CLAIMS = 3

STRONG_TYPES = {"RCT", "Meta-Analysis", "Systematic Review"}
MODERATE_TYPES = {"Observational", "Case-Control", "Cohort"}
WEAK_TYPES = {"Case Study", "Opinion", "Editorial"}


class EvidenceExtractor:
    def __init__(self, classifier: Optional[StudyClassifier] = None):
        self.classifier = classifier or StudyClassifier()

    async def extract_evidence(
        self,
        papers: List[Paper],
        qwen_client: QwenClient
    ) -> List[Dict]:
        logger.info("Extracting evidence...")
        if not papers:
            return []

        classifications = await self.classifier.classify_studies(papers, qwen_client)
        type_by_id = {
            item["paper"].paper_id: item["study_type"]
            for item in classifications
        }

        evidence = []
        for paper in papers:
            claims = await self._extract_claims(paper, qwen_client)
            study_type = type_by_id.get(paper.paper_id, "Other")
            strength = self._rate_strength(study_type, paper.citation_count)
            if strength == "WEAK":
                continue
            evidence.append({
                "paper": paper,
                "claims": claims,
                "strength": strength
            })

        return evidence

    async def _extract_claims(self, paper: Paper, qwen_client: QwenClient) -> List[str]:
        abstract = paper.abstract or ""
        prompt = (
            "Extract 1-3 key findings from this paper. "
            f"Title: {paper.title}. Abstract: {abstract}. Return as JSON array."
        )
        response = await qwen_client.complete(prompt)
        return self._parse_json_list(response.content)[:MAX_CLAIMS]

    def _rate_strength(self, study_type: str, citations: int) -> str:
        normalized = study_type.strip()
        if citations < MODERATE_CITATION_THRESHOLD:
            return "WEAK"
        if normalized in WEAK_TYPES:
            return "WEAK"
        if normalized in STRONG_TYPES and citations >= STRONG_CITATION_THRESHOLD:
            return "STRONG"
        if normalized in MODERATE_TYPES:
            return "MODERATE"
        if MODERATE_CITATION_THRESHOLD <= citations <= STRONG_CITATION_THRESHOLD - 1:
            return "MODERATE"
        return "WEAK"

    def _parse_json_list(self, content: str) -> List[str]:
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            data = []

        if isinstance(data, list):
            return [str(item).strip() for item in data if str(item).strip()]
        if isinstance(data, str) and data.strip():
            return [data.strip()]
        return []
