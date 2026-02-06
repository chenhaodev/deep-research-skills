import difflib
import string
from typing import List

from deep_research.api.models import Paper


class DeduplicationEngine:
    def deduplicate(self, papers: List[Paper]) -> List[Paper]:
        seen_ids = set()
        seen_titles = []
        result = []

        for paper in papers:
            external_ids = paper.external_ids
            if external_ids.doi and external_ids.doi in seen_ids:
                continue
            if external_ids.pmid and external_ids.pmid in seen_ids:
                continue
            if external_ids.s2_id and external_ids.s2_id in seen_ids:
                continue

            normalized_title = self._normalize_title(paper.title)
            is_duplicate_title = False
            for existing_title in seen_titles:
                similarity = difflib.SequenceMatcher(
                    None,
                    normalized_title,
                    existing_title
                ).ratio()
                if similarity > 0.95:
                    is_duplicate_title = True
                    break

            if is_duplicate_title:
                continue

            result.append(paper)
            seen_titles.append(normalized_title)
            if external_ids.doi:
                seen_ids.add(external_ids.doi)
            if external_ids.pmid:
                seen_ids.add(external_ids.pmid)
            if external_ids.s2_id:
                seen_ids.add(external_ids.s2_id)

        return result

    def _normalize_title(self, title: str) -> str:
        normalized = (title or "").lower().translate(
            str.maketrans("", "", string.punctuation)
        )
        return " ".join(normalized.split())
