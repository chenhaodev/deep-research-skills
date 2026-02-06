# Synthesis Methods SOP

## Purpose
This document defines the Standard Operating Procedure (SOP) for analyzing eligible papers. It specifies algorithms for classifying study types, rating evidence strength, assigning quality badges, and extracting key claims.

## 1. Evidence Strength Rating
**Objective:** Assign a confidence level to the evidence provided by a paper.
**Algorithm:** Evaluate based on Study Type AND Citation Count.

### Level: STRONG
*   **Criteria:**
    *   Study Type = `RCT` OR `Meta-Analysis` OR `Systematic Review`
    *   AND Citation Count ≥ 100
*   **Description:** High-quality evidence from rigorous methodologies with significant community validation.

### Level: MODERATE
*   **Criteria:**
    *   Study Type = `Observational` OR `Case-Control` OR `Cohort`
    *   OR (Any Study Type with Citation Count between 50 and 99)
*   **Description:** Reliable evidence but may lack causal proof or broad community validation.

### Level: WEAK (Filter Out)
*   **Criteria:**
    *   Study Type = `Case Study` OR `Opinion` OR `Editorial`
    *   OR Citation Count < 50
*   **Action:** These papers should generally be excluded from the final consensus calculation unless the total pool of papers is very small (< 10).

## 2. Study Classification
**Objective:** Determine the methodology used in the paper.
**Method:** Keyword Matching with LLM Fallback.

### Step 2.1: Keyword Matching (Case-Insensitive)
Check `title` and `abstract` for these exact phrases:

*   **RCT:** "randomized controlled trial", "RCT", "random assignment", "randomized trial"
*   **Meta-Analysis:** "meta-analysis", "systematic review and meta-analysis"
*   **Systematic Review:** "systematic review", "literature review" (only if "protocol" is also present)
*   **Observational:** "observational study", "cohort study", "case-control", "cross-sectional", "longitudinal study"

### Step 2.2: LLM Fallback
If no keywords match, use the following prompt:
> "Classify the study type of the paper titled '[title]' with abstract '[abstract]'. Output EXACTLY one of: RCT, Meta-Analysis, Systematic Review, Observational, Case Study, Opinion, Other."

## 3. Quality Badges
**Objective:** Highlight exceptional papers based on bibliometrics.

*   **Badge: RIGOROUS JOURNAL**
    *   **Rule:** The journal where the paper was published has a total citation count > 10,000 (proxy for impact factor/prestige).
    *   **Data Source:** Journal metadata from search provider.

*   **Badge: HIGHLY CITED**
    *   **Rule:** The paper itself has > 100 citations.
    *   **Significance:** Indicates high influence in the field.

## 4. Key Claim Extraction
**Objective:** Extract the core findings relevant to the user's query.

*   **Limit:** Extract maximum 1-3 distinct claims per paper.
*   **Format:** Single sentence per claim.
*   **Constraint:** Claims must be supported by results, not just stated in the introduction.
*   **Prompt:**
    > "Extract the top 1-3 core findings from this abstract that answer the question: '[user_query]'. Return as a JSON list of strings."

## 5. Example Synthesis Entry
```json
{
  "paper_id": "10.1038/s41586-023-00000-x",
  "study_type": "RCT",
  "evidence_strength": "STRONG",
  "citations": 150,
  "badges": ["HIGHLY CITED", "RIGOROUS JOURNAL"],
  "claims": [
    "Model A outperforms Model B by 15% on reasoning tasks.",
    "Fine-tuning on synthetic data reduces hallucination rates."
  ]
}
```

## 6. Parameter Specifications
| Parameter | Value | Description |
| :--- | :--- | :--- |
| `STRONG_CITATION_THRESHOLD` | 100 | Min citations for Strong rating (with correct type) |
| `MODERATE_CITATION_THRESHOLD` | 50 | Min citations for Moderate rating |
| `JOURNAL_IMPACT_THRESHOLD` | 10000 | Total journal citations for Rigorous Journal badge |
| `MAX_CLAIMS` | 3 | Max claims to extract per paper |
