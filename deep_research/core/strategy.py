import json
from typing import Dict, List, Optional

from deep_research.api.models import Paper
from deep_research.api.qwen import QwenClient
from deep_research.config import Config
from deep_research.utils.logging import get_logger


logger = get_logger(__name__)


class StrategyGenerator:
    def __init__(self, qwen_client: Optional[QwenClient] = None):
        if qwen_client is None:
            config = Config()
            qwen_client = QwenClient(config.qwen)
        self.qwen_client = qwen_client

    async def generate_strategy(
        self,
        query: str,
        survey_results: List[Paper]
    ) -> Dict[str, List[str]]:
        synonyms = await self._extract_synonyms(query, survey_results)
        base_terms = self._build_base_terms(query, synonyms, max_terms=4)

        strategies = {
            "bottlenecks": self._build_pattern_queries(
                base_terms,
                "(limitation OR bottleneck OR challenge OR barrier OR constraint)",
                query
            ),
            "whitespace": self._build_pattern_queries(
                base_terms,
                "(gap OR unexplored OR future research OR opportunity OR open problem)",
                query
            ),
            "scenarios": self._build_pattern_queries(
                base_terms,
                "(application OR use case OR implementation OR deployment OR real-world)",
                query
            ),
            "terminology": self._build_terminology_queries(base_terms, query),
            "international": self._build_pattern_queries(
                base_terms,
                "(country OR regional OR international OR global OR cross-cultural)",
                query
            ),
            "foundational": self._build_pattern_queries(
                base_terms,
                "(review OR survey OR foundational OR state-of-the-art OR meta-analysis)",
                query
            )
        }

        return strategies

    async def _extract_synonyms(self, query: str, survey_results: List[Paper]) -> List[str]:
        abstracts = []
        for paper in survey_results[:10]:
            if paper.abstract:
                abstracts.append(paper.abstract.strip())
            elif paper.title:
                abstracts.append(paper.title.strip())

        prompt = (
            f"Extract 3-5 alternative terms, acronyms, or related phrases for the topic: '{query}'. "
            "Return a JSON array of strings only.\n\n"
            "Context:\n"
            + "\n".join(abstracts)
        )

        response = await self.qwen_client.complete(prompt, max_tokens=256, temperature=0.2)
        synonyms = self._parse_synonyms(response.content)

        logger.info(f"Strategy: extracted {len(synonyms)} synonyms")
        return synonyms

    def _parse_synonyms(self, content: str) -> List[str]:
        try:
            parsed = json.loads(content)
            if isinstance(parsed, list):
                return self._clean_terms(parsed)
            if isinstance(parsed, dict):
                for key in ("synonyms", "terms", "related_terms"):
                    if key in parsed and isinstance(parsed[key], list):
                        return self._clean_terms(parsed[key])
        except json.JSONDecodeError:
            pass

        fallback_terms = [term.strip() for term in content.split(",") if term.strip()]
        return self._clean_terms(fallback_terms)

    def _clean_terms(self, terms: List[str]) -> List[str]:
        seen = set()
        cleaned = []
        for term in terms:
            normalized = term.strip()
            if not normalized:
                continue
            key = normalized.lower()
            if key in seen:
                continue
            seen.add(key)
            cleaned.append(normalized)
        return cleaned

    def _build_base_terms(self, query: str, synonyms: List[str], max_terms: int = 4) -> List[str]:
        terms = [query]
        for synonym in synonyms:
            if synonym.lower() == query.lower():
                continue
            terms.append(synonym)
            if len(terms) >= max_terms:
                break
        return terms

    def _build_pattern_queries(self, terms: List[str], pattern: str, query: str) -> List[str]:
        queries = [f"{term} AND {pattern}" for term in terms]
        return self._ensure_query_count(queries, query, pattern)

    def _build_terminology_queries(self, terms: List[str], query: str) -> List[str]:
        queries: List[str] = []

        if len(terms) >= 2:
            queries.append(" OR ".join(terms))
            queries.append(f"{terms[0]} OR {terms[1]}")
            queries.append(f"{terms[0]} OR {terms[-1]}")
            if len(terms) >= 3:
                queries.append(f"{terms[1]} OR {terms[2]}")
        else:
            queries.extend([query, f"({query})", f"\"{query}\""])

        return self._ensure_query_count(queries, query)

    def _ensure_query_count(
        self,
        queries: List[str],
        query: str,
        pattern: Optional[str] = None
    ) -> List[str]:
        unique_queries = []
        seen = set()
        for q in queries:
            if q not in seen:
                seen.add(q)
                unique_queries.append(q)

        while len(unique_queries) < 3:
            if pattern:
                unique_queries.append(f"\"{query}\" AND {pattern}")
            else:
                unique_queries.append(f"({query})")

        return unique_queries[:4]
