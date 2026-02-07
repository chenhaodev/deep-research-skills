import json
from typing import Dict, List

from deep_research.api.models import Paper
from deep_research.api.qwen import QwenClient
from deep_research.utils.logging import get_logger


logger = get_logger(__name__)

MATRIX_DIMENSION = 5


class GapAnalyzer:
    async def analyze_gaps(self, papers: List[Paper], qwen_client: QwenClient) -> Dict:
        logger.info("Analyzing gaps...")
        if not papers:
            return {"themes": [], "technologies": [], "matrix": [], "gaps": []}

        abstracts_text = self._format_abstracts(papers)

        theme_prompt = (
            f"Analyze these {len(papers)} abstracts. List the top 5 recurring research "
            "themes or application scenarios. Return as a JSON list.\n\n"
            f"{abstracts_text}"
        )
        tech_prompt = (
            f"Analyze these {len(papers)} abstracts. List the top 5 distinct technologies, "
            "models, or methodologies used. Return as a JSON list.\n\n"
            f"{abstracts_text}"
        )

        themes_response = await qwen_client.complete(theme_prompt)
        tech_response = await qwen_client.complete(tech_prompt)

        themes = self._normalize_list(self._parse_json_list(themes_response.content), "Theme")
        technologies = self._normalize_list(self._parse_json_list(tech_response.content), "Tech")

        matrix = []
        gaps = []
        for theme in themes:
            row = []
            for tech in technologies:
                count = self._count_intersection(papers, theme, tech)
                row.append(count)
                if count == 0:
                    gaps.append({"theme": theme, "tech": tech, "opportunity": ""})
            matrix.append(row)

        opportunities = []
        if gaps:
            gap_list = [f"{gap['theme']} × {gap['tech']}" for gap in gaps]
            opportunity_prompt = (
                "The following intersections have no research papers: "
                f"{gap_list}. Given the properties of these technologies and themes, "
                "suggest 3 specific research opportunities or hypotheses to test in these gaps."
            )
            response = await qwen_client.complete(opportunity_prompt)
            opportunities = self._parse_json_list(response.content)
            if not opportunities and response.content.strip():
                opportunities = [response.content.strip()]

        for index, gap in enumerate(gaps):
            if opportunities:
                gap["opportunity"] = opportunities[index % len(opportunities)]

        return {
            "themes": themes,
            "technologies": technologies,
            "matrix": matrix,
            "gaps": gaps
        }

    def _format_abstracts(self, papers: List[Paper]) -> str:
        lines = []
        for index, paper in enumerate(papers, start=1):
            abstract = paper.abstract or ""
            lines.append(f"Abstract {index}: {abstract}")
        return "\n".join(lines)

    def _count_intersection(self, papers: List[Paper], theme: str, tech: str) -> int:
        theme_lower = theme.lower()
        tech_lower = tech.lower()
        count = 0
        for paper in papers:
            text = f"{paper.title} {paper.abstract or ''}".lower()
            if theme_lower in text and tech_lower in text:
                count += 1
        return count

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

    def _normalize_list(self, values: List[str], label: str) -> List[str]:
        normalized = values[:MATRIX_DIMENSION]
        while len(normalized) < MATRIX_DIMENSION:
            normalized.append(f"{label} {len(normalized) + 1}")
        return normalized
