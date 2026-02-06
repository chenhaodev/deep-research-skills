# Screening Protocol SOP

## Purpose
This document defines the Standard Operating Procedure (SOP) for filtering raw search results into a high-quality dataset for analysis. The protocol uses a strict three-stage funnel: Deduplication → Quality Screening → Relevance Screening.

## 1. The Screening Funnel
The screening process MUST proceed in this exact order. A paper must pass the current stage to proceed to the next.

1.  **Deduplication:** Remove technical duplicates.
2.  **Quality Check:** Remove low-quality or malformed metadata.
3.  **Relevance Check:** Remove off-topic content based on semantic similarity.

## 2. Stage 1: Deduplication Rules
**Objective:** Ensure each unique paper appears only once.

### Rule 1.1: Exact ID Matching
Check for matches in standard identifiers.
*   **Priority Order:** DOI > PMID > S2 ID.
*   **Algorithm:**
    1.  If `DOI` exists and matches another record, keep the record with more complete metadata.
    2.  Else if `PMID` exists and matches, deduplicate.
    3.  Else if `S2 ID` exists and matches, deduplicate.

### Rule 1.2: Title Similarity
Check for fuzzy matches in titles to catch duplicates with missing IDs.
*   **Preprocessing:** Convert to lowercase, remove all punctuation, remove extra whitespace.
*   **Metric:** Levenshtein distance or Jaccard similarity.
*   **Threshold:** > 95% similarity.
*   **Action:** If similarity > 95%, treat as duplicate. Keep the version with the most recent scrape date or most complete abstract.

## 3. Stage 2: Quality Criteria
**Objective:** Filter out metadata stubs, non-English content, and outdated work.
**All criteria must be met (AND logic).**

*   **Criterion 2.1: Abstract Presence**
    *   **Rule:** `abstract` field MUST NOT be null or empty string.
    *   **Action:** Reject if missing.

*   **Criterion 2.2: Abstract Length**
    *   **Rule:** Word count of `abstract` MUST be ≥ 50 words.
    *   **Action:** Reject if < 50 words (filters out "Abstract not available" placeholders).

*   **Criterion 2.3: Language**
    *   **Rule:** Language detection on title + abstract MUST return 'en' (English).
    *   **Action:** Reject if non-English.

*   **Criterion 2.4: Date Range**
    *   **Rule:** Publication date MUST be within the last 3 years (unless user overrides).
    *   **Default:** `current_date - 3 years`.
    *   **Action:** Reject if older.

## 4. Stage 3: Relevance Screening
**Objective:** Ensure the paper actually addresses the user's research topic.

*   **Method:** Semantic Similarity (Embedding-based).
*   **Input:** Concatenation of `title` + `abstract`.
*   **Query:** The user's original research question or topic description.
*   **Threshold:** 0.6 (Cosine Similarity).
*   **Algorithm:**
    1.  Generate embedding for User Query ($E_q$).
    2.  Generate embedding for Paper ($E_p$).
    3.  Calculate Cosine Similarity $S = \frac{E_q \cdot E_p}{\|E_q\| \|E_p\|}$.
    4.  If $S < 0.6$, Reject.
    5.  If $S \ge 0.6$, Accept.

## 5. Example Screening Log
The system must log the reason for every rejection.

```json
[
  {
    "id": "paper_123",
    "status": "REJECTED",
    "stage": "Quality",
    "reason": "Abstract length < 50 words (count: 12)"
  },
  {
    "id": "paper_456",
    "status": "REJECTED",
    "stage": "Relevance",
    "reason": "Similarity score 0.45 < threshold 0.6"
  },
  {
    "id": "paper_789",
    "status": "ACCEPTED",
    "stage": "Final",
    "score": 0.82
  }
]
```

## 6. Parameter Specifications
| Parameter | Value | Description |
| :--- | :--- | :--- |
| `TITLE_SIMILARITY_THRESHOLD` | 0.95 | Threshold for fuzzy title deduplication |
| `MIN_ABSTRACT_WORDS` | 50 | Minimum word count for valid abstract |
| `RELEVANCE_THRESHOLD` | 0.6 | Minimum cosine similarity score |
| `DEFAULT_DATE_RANGE_YEARS` | 3 | Default lookback period |
