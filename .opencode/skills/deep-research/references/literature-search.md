# Literature Search Strategy SOP

## Purpose
This document defines the Standard Operating Procedure (SOP) for the "Deep Research" literature search phase. It specifies exact query construction patterns, execution limits, and citation graph traversal rules to ensure high recall and diverse coverage of the topic.

## 1. Multi-Angle Search Strategy
To avoid "filter bubbles" and ensure comprehensive coverage, the search agent MUST generate queries from 6 distinct angles.

### Angle 1: Bottlenecks & Limitations
**Goal:** Identify problems, challenges, and constraints in the current state of the art.
**Query Pattern:**
```
[topic] AND (limitation OR bottleneck OR challenge OR barrier OR constraint)
```
**Example:** `LLM reasoning AND (limitation OR bottleneck OR challenge)`

### Angle 2: White Space & Gaps
**Goal:** Find explicitly identified gaps, future research directions, and unexplored areas.
**Query Pattern:**
```
[topic] AND (gap OR unexplored OR future research OR opportunity OR open problem)
```
**Example:** `LLM reasoning AND (gap OR unexplored OR future research)`

### Angle 3: Scenarios & Applications
**Goal:** Discover how the topic is applied in practice and specific use cases.
**Query Pattern:**
```
[topic] AND (application OR use case OR implementation OR deployment OR real-world)
```
**Example:** `LLM reasoning AND (application OR use case OR implementation)`

### Angle 4: Terminology & Synonyms
**Goal:** Expand search scope by using alternative terms, acronyms, and related concepts.
**Query Pattern:**
```
[synonym_1] OR [synonym_2] OR [related_term]
```
**Example:** `(Large Language Model OR Foundation Model) AND (reasoning OR chain-of-thought)`

### Angle 5: International & Regional
**Goal:** Capture global perspectives and non-Western research contexts.
**Query Pattern:**
```
[topic] AND (country OR regional OR international OR global OR cross-cultural)
```
**Example:** `LLM reasoning AND (country OR regional OR international)`

### Angle 6: Foundational & Reviews
**Goal:** Anchor the research in established knowledge and broad overviews.
**Query Pattern:**
```
[topic] AND (review OR survey OR foundational OR state-of-the-art OR meta-analysis)
```
**Example:** `LLM reasoning AND (review OR survey OR foundational)`

## 2. Search Execution Rules
The search agent must adhere to the following strict execution limits to balance breadth and depth.

*   **Queries per Angle:** Generate exactly 3-4 distinct queries for each of the 6 angles.
*   **Total Queries:** Maximum 20-25 queries per search session.
*   **Results per Query:** Fetch top 10 results per query.
*   **Deduplication:** Perform initial deduplication during the search phase based on URL or Title to avoid redundant processing.

## 3. Citation Graph Exploration
To find high-impact papers that might be missed by keyword search, the agent MUST traverse the citation graph.

*   **Depth:** Maximum 2 levels.
    *   **Level 0:** Seed papers found via keyword search.
    *   **Level 1:** Papers citing Level 0 papers (Forward) AND papers cited by Level 0 papers (Backward).
    *   **Level 2:** (Optional) High-impact papers connected to Level 1, only if Level 1 yields < 10 relevant results.
*   **Selection Criteria for Traversal:**
    *   Only traverse from papers with > 50 citations (if older than 2 years).
    *   Only traverse from papers published in the last 12 months (regardless of citations).

## 4. Example Output Structure
The search module should output a list of candidate papers in JSON format:

```json
[
  {
    "source_query": "LLM reasoning AND (limitation OR bottleneck)",
    "angle": "Bottlenecks",
    "title": "Reasoning Limitations in Large Language Models",
    "url": "https://arxiv.org/abs/xxxx.xxxxx",
    "year": 2024,
    "citation_count": 45
  },
  ...
]
```

## 5. Parameter Specifications
| Parameter | Value | Description |
| :--- | :--- | :--- |
| `MAX_QUERIES_TOTAL` | 25 | Hard limit on total search queries |
| `QUERIES_PER_ANGLE` | 3-4 | Target range for query generation |
| `CITATION_DEPTH` | 2 | Max levels of citation graph traversal |
| `MIN_CITATIONS_FOR_TRAVERSAL` | 50 | Threshold to use a paper as a seed node |
