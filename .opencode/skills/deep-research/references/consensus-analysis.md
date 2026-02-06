# Consensus & Gap Analysis SOP

## Purpose
This document defines the Standard Operating Procedure (SOP) for synthesizing individual paper findings into aggregate metrics. It specifies the exact algorithms for calculating scientific consensus and generating a "White Space" gap analysis matrix.

## 1. Consensus Quantification Algorithm
**Objective:** Determine the level of agreement in the literature regarding a specific Yes/No question.

### Step 1: Filtering
Identify papers that actually address the question.
*   **Prompt:** "Does the paper '[title]' with abstract '[abstract]' provide an answer or evidence regarding the question: '[question]'? Answer YES or NO."
*   **Action:** Discard papers where answer is NO.

### Step 2: Extraction
Classify the stance of each relevant paper.
*   **Prompt:** "What is this paper's answer to the question: '[question]'? Based on the abstract, choose exactly one: YES, NO, MIXED, POSSIBLY."
*   **Definitions:**
    *   `YES`: Strong affirmative evidence.
    *   `NO`: Strong negative evidence.
    *   `MIXED`: Conflicting results or conditional findings.
    *   `POSSIBLY`: Hypothesized but not strictly proven, or weak evidence.

### Step 3: Calculation
Compute the percentage distribution.
*   $N_{total} = Count(YES) + Count(NO) + Count(MIXED) + Count(POSSIBLY)$
*   $P_{category} = \frac{Count(category)}{N_{total}} \times 100$

### Step 4: Confidence Score
Calculate a confidence score for the consensus based on sample size.
*   **Formula:** $Confidence = \min(1.0, \frac{N_{total}}{10})$
*   **Interpretation:**
    *   $\ge 10$ papers: 100% Confidence (1.0)
    *   $5$ papers: 50% Confidence (0.5)
    *   $< 5$ papers: Low Confidence

### Step 5: Error Handling
*   **Rule:** If $N_{total} < 5$, flag the consensus as "INSUFFICIENT DATA". Do not display a percentage chart without this warning.

## 2. Gap Analysis Matrix Algorithm
**Objective:** Identify unexplored intersections between research themes and technologies.

### Step 1: Theme Extraction
Extract the top 5 research themes/scenarios from the entire set of included papers.
*   **Prompt:** "Analyze these [N] abstracts. List the top 5 recurring research themes or application scenarios. Return as a JSON list."

### Step 2: Technology/Method Extraction
Extract the top 5 technologies or methodologies used.
*   **Prompt:** "Analyze these [N] abstracts. List the top 5 distinct technologies, models, or methodologies used. Return as a JSON list."

### Step 3: Matrix Construction
Build a 5x5 matrix where:
*   Rows = Themes
*   Columns = Technologies
*   **Cell Value:** List of Paper IDs that belong to the intersection of (Row, Column).
*   **Check:** For each cell (Theme $T$, Tech $M$), check if any paper contains BOTH keywords/concepts.

### Step 4: Gap Identification
*   **Rule:** Mark any cell with 0 papers as a **GAP**.
*   **Rule:** Mark any cell with 1-2 papers as **THIN**.

### Step 5: Opportunity Generation
Generate research opportunities based on the gaps.
*   **Prompt:** "The following intersections have no research papers: [List of Gaps]. Given the properties of these technologies and themes, suggest 3 specific research opportunities or hypotheses to test in these gaps."

## 3. Example Outputs

### Consensus Output
```json
{
  "question": "Do LLMs improve coding productivity?",
  "total_papers": 14,
  "confidence": 1.0,
  "distribution": {
    "YES": 57,
    "MIXED": 36,
    "POSSIBLY": 7,
    "NO": 0
  }
}
```

### Gap Matrix (Partial)
| | Transformer | LSTM | RNN |
| :--- | :--- | :--- | :--- |
| **Healthcare** | [Paper_1, Paper_5] | [Paper_3] | **GAP** |
| **Finance** | [Paper_2] | **GAP** | **GAP** |

## 4. Parameter Specifications
| Parameter | Value | Description |
| :--- | :--- | :--- |
| `CONSENSUS_MIN_PAPERS` | 5 | Min papers to report consensus without warning |
| `CONSENSUS_FULL_CONFIDENCE` | 10 | Papers needed for 1.0 confidence score |
| `MATRIX_DIMENSION` | 5 | Size of gap analysis matrix (5x5) |
