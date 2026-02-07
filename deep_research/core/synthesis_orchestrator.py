from typing import Dict, List, Optional

from deep_research.api.models import Paper
from deep_research.api.qwen import QwenClient
from deep_research.core.classifier import StudyClassifier
from deep_research.core.consensus import ConsensusAnalyzer
from deep_research.core.evidence import EvidenceExtractor
from deep_research.core.gap_analysis import GapAnalyzer
from deep_research.core.report import ReportGenerator
from deep_research.utils.logging import get_logger


logger = get_logger(__name__)


class SynthesisOrchestrator:
    def __init__(
        self,
        evidence_extractor: Optional[EvidenceExtractor] = None,
        classifier: Optional[StudyClassifier] = None,
        consensus_analyzer: Optional[ConsensusAnalyzer] = None,
        gap_analyzer: Optional[GapAnalyzer] = None,
        report_generator: Optional[ReportGenerator] = None
    ):
        self.evidence_extractor = evidence_extractor or EvidenceExtractor()
        self.classifier = classifier or StudyClassifier()
        self.consensus_analyzer = consensus_analyzer or ConsensusAnalyzer()
        self.gap_analyzer = gap_analyzer or GapAnalyzer()
        self.report_generator = report_generator or ReportGenerator()

    async def synthesize(
        self,
        papers: List[Paper],
        query: str,
        qwen_client: QwenClient
    ) -> Dict:
        logger.info("Synthesis: Extracting evidence...")
        evidence = await self.evidence_extractor.extract_evidence(papers, qwen_client)

        logger.info("Synthesis: Classifying studies...")
        classifications = await self.classifier.classify_studies(papers, qwen_client)

        consensus = {}
        if self._is_yes_no_question(query):
            logger.info("Synthesis: Quantifying consensus...")
            consensus = await self.consensus_analyzer.quantify_consensus(
                papers,
                query,
                qwen_client
            )

        logger.info("Synthesis: Analyzing gaps...")
        gaps = await self.gap_analyzer.analyze_gaps(papers, qwen_client)

        logger.info("Synthesis: Generating report...")
        report = self.report_generator.generate_report(papers, evidence, consensus, gaps)

        return {
            "evidence": evidence,
            "classifications": classifications,
            "consensus": consensus,
            "gaps": gaps,
            "report": report
        }

    def _is_yes_no_question(self, query: str) -> bool:
        normalized = query.strip().lower()
        if not normalized:
            return False
        if "yes/no" in normalized or "yes or no" in normalized:
            return True
        if not normalized.endswith("?"):
            return False
        leading = normalized.split()[0]
        return leading in {
            "is",
            "are",
            "am",
            "was",
            "were",
            "do",
            "does",
            "did",
            "can",
            "could",
            "will",
            "would",
            "should",
            "has",
            "have",
            "had",
            "may",
            "might",
            "must"
        }
