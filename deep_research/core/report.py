from typing import Dict, List

from deep_research.api.models import Paper
from deep_research.utils.logging import get_logger


logger = get_logger(__name__)

METER_WIDTH = 24


class ReportGenerator:
    def generate_report(
        self,
        papers: List[Paper],
        evidence: List[Dict],
        consensus: Dict,
        gaps: Dict
    ) -> str:
        logger.info("Generating report...")
        ref_map = {paper.paper_id: index + 1 for index, paper in enumerate(papers)}
        title = consensus.get("question") if consensus else "Research Report"

        lines = [
            f"# {title}",
            "",
            "## Introduction",
            "",
            "Brief overview of the research question and why it matters.",
            "",
            "## Methods",
            "",
            "**Search Strategy:**",
            "- Databases: Semantic Scholar, PubMed",
            f"- Papers screened: {len(papers)} included",
            "",
            "**Inclusion Criteria:**",
            "- English language",
            "- Has abstract",
            "- Semantic relevance score ≥ 0.6",
            "",
            "## Results",
            "",
            "### Overview",
            f"Included {len(papers)} papers after screening.",
            "",
            "### Evidence Summary"
        ]

        for item in evidence:
            paper = item["paper"]
            ref = ref_map.get(paper.paper_id)
            for claim in item.get("claims", []):
                lines.append(f"- {claim} [{ref}]")

        if evidence:
            lines.append("")

        if consensus and consensus.get("question"):
            yes = consensus.get("yes_percent", 0.0)
            no = consensus.get("no_percent", 0.0)
            mixed = consensus.get("mixed_percent", 0.0)
            possibly = consensus.get("possibly_percent", 0.0)
            total = consensus.get("total_papers", 0)
            confidence = consensus.get("confidence", 0.0)

            lines.extend([
                "### Consensus Analysis",
                f"**Question:** {consensus.get('question')}",
                "",
                "**Result:**",
                f"- YES: {yes:.1f}% (N={self._count_from_percent(yes, total)} papers)",
                f"- NO: {no:.1f}% (N={self._count_from_percent(no, total)} papers)",
                f"- MIXED: {mixed:.1f}% (N={self._count_from_percent(mixed, total)} papers)",
                f"- POSSIBLY: {possibly:.1f}% (N={self._count_from_percent(possibly, total)} papers)",
                f"**Confidence:** {confidence:.2f} (based on N={total} papers)",
                "",
                self._render_consensus_meter(consensus),
                ""
            ])

        if gaps:
            lines.extend([
                "### Gap Analysis Matrix",
                "",
                self._render_gap_table(gaps),
                "",
                "**White Space Opportunities:**"
            ])
            for index, gap in enumerate(gaps.get("gaps", []), start=1):
                lines.append(
                    f"{index}. {gap['theme']} × {gap['tech']}: {gap.get('opportunity', '')}"
                )
            lines.append("")

        lines.extend([
            "## Discussion",
            "",
            "### Key Takeaways",
            "1. Consensus and gaps highlight the dominant findings.",
            "2. Evidence strength varies by study type and citations.",
            "3. Opportunities emerge at understudied intersections.",
            "",
            "### Limitations",
            "- Limited to English-language abstracts",
            "- Semantic search may miss domain-specific terminology",
            "",
            "### Future Directions",
            "Further studies should focus on gaps identified above.",
            "",
            "## References",
            ""
        ])

        lines.extend(self._render_references(papers))
        return "\n".join(lines)

    def _render_references(self, papers: List[Paper]) -> List[str]:
        references = []
        for index, paper in enumerate(papers, start=1):
            authors = self._format_authors(paper)
            year = paper.year if paper.year is not None else "n.d."
            venue = paper.venue or "Unknown Journal"
            doi = paper.external_ids.doi if paper.external_ids.doi else "N/A"
            references.append(
                f"[{index}] {authors}. ({year}). {paper.title}. {venue}. DOI: {doi}"
            )
        return references

    def _format_authors(self, paper: Paper) -> str:
        if not paper.authors:
            return "Unknown"
        if len(paper.authors) == 1:
            return paper.authors[0].name
        if len(paper.authors) == 2:
            return f"{paper.authors[0].name}, {paper.authors[1].name}"
        return f"{paper.authors[0].name}, et al."

    def _render_consensus_meter(self, consensus: Dict) -> str:
        yes = consensus.get("yes_percent", 0.0)
        no = consensus.get("no_percent", 0.0)
        mixed = consensus.get("mixed_percent", 0.0)
        possibly = consensus.get("possibly_percent", 0.0)
        total = consensus.get("total_papers", 0)
        confidence = consensus.get("confidence", 0.0)

        lines = [
            "```",
            "┌─────────────────────────────────────────────────┐",
            "│         CONSENSUS METER                         │",
            f"│  Question: {consensus.get('question', ''):<35}│",
            "├─────────────────────────────────────────────────┤",
            self._meter_line("YES", yes, total),
            self._meter_line("POSSIBLY", possibly, total),
            self._meter_line("MIXED", mixed, total),
            self._meter_line("NO", no, total),
            "├─────────────────────────────────────────────────┤",
            f"│  Total Papers Analyzed: {total:<21}│",
            f"│  Confidence: {int(confidence * 100):>3}% (based on N={total})     │",
            "└─────────────────────────────────────────────────┘",
            "```"
        ]
        return "\n".join(lines)

    def _meter_line(self, label: str, percent: float, total: int) -> str:
        filled = int(round((percent / 100) * METER_WIDTH)) if total else 0
        bar = "█" * filled + "░" * (METER_WIDTH - filled)
        count = self._count_from_percent(percent, total)
        return f"│  {label:<8} {bar}  {percent:>3.0f}%  ({count})   │"

    def _render_gap_table(self, gaps: Dict) -> str:
        themes = gaps.get("themes", [])
        technologies = gaps.get("technologies", [])
        matrix = gaps.get("matrix", [])

        header = "| Theme/Tech | " + " | ".join(technologies) + " |"
        divider = "|" + "------------|" * (len(technologies) + 1)
        lines = [header, divider]
        for theme, row in zip(themes, matrix):
            cells = ["GAP" if value == 0 else str(value) for value in row]
            lines.append("| " + " | ".join([theme] + cells) + " |")
        return "\n".join(lines)

    def _count_from_percent(self, percent: float, total: int) -> int:
        if total == 0:
            return 0
        return int(round((percent / 100) * total))
