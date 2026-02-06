# Research Report Templates

## Full Report Structure

```markdown
# [Research Question Title]

## Introduction

[Brief overview of the research question and why it matters]

[Context from initial survey]

## Methods

**Search Strategy:**
- Databases: Semantic Scholar, PubMed
- Search dates: [Date range]
- Total searches: [N] distinct queries across [M] angles
- Papers screened: [N identified] → [M after dedup] → [K after relevance screening] → [J included]

**Inclusion Criteria:**
- English language
- Published within [date range]
- Has abstract
- Semantic relevance score ≥ 0.6

**Search Angles:**
1. Bottleneck technologies
2. White space opportunities
3. Practical scenarios
4. Alternative terminology
5. International models
6. Foundational work

## Results

### Overview
[Summary paragraph of key findings]

### Themes

#### [Theme 1 Name]
[Description of this research theme]

**Key Papers:**
- Finding A [1]
- Finding B [2]
- Finding C [3]

#### [Theme 2 Name]
...

### Consensus Analysis
[If binary question was asked]

**Question:** [Yes/No question]

**Result:**
- YES: [X]% (N=[n] papers)
- NO: [Y]% (N=[m] papers)
- MIXED: [Z]% (N=[k] papers)

**Confidence:** [confidence score] (based on N=[total] papers analyzed)

### Gap Analysis

| Theme/Scenario | Technology 1 | Technology 2 | Technology 3 | Technology 4 | Technology 5 |
|---------------|-------------|-------------|-------------|-------------|-------------|
| **Scenario 1** | ✓ (N=5) | GAP | ✓ (N=3) | GAP | ✓ (N=2) |
| **Scenario 2** | ✓ (N=8) | ✓ (N=1) | GAP | GAP | ✓ (N=4) |
| **Scenario 3** | GAP | ✓ (N=2) | ✓ (N=6) | ✓ (N=1) | GAP |
| **Scenario 4** | ✓ (N=3) | GAP | GAP | ✓ (N=5) | ✓ (N=2) |
| **Scenario 5** | ✓ (N=4) | ✓ (N=3) | ✓ (N=2) | GAP | GAP |

**White Space Opportunities:**
1. [Intersection with no research - research opportunity description]
2. [Another gap - what could be explored]
3. ...

## Discussion

### Key Takeaways
1. [Main finding 1]
2. [Main finding 2]
3. [Main finding 3]

### Limitations
- [Limitation 1: e.g., limited to English papers]
- [Limitation 2: e.g., semantic search may miss domain-specific terminology]

### Future Directions
[Suggested research based on gaps identified]

## References

[1] Author A, Author B. (Year). Title of paper. *Journal Name*, Volume(Issue), pages. DOI: 10.xxxx/xxxxx

[2] Author C, et al. (Year). Another paper title. *Journal*, vol(issue), pages. DOI: 10.yyyy/yyyyy

[3] ...
```

## Evidence Table Template

| Paper | Study Type | Evidence Strength | Key Claim | Reasoning |
|-------|-----------|------------------|-----------|----------|
| [1] | RCT | Strong | [Main finding] | [Why this evidence is strong] |
| [2] | Meta-Analysis | Strong | [Conclusion] | [Based on N=X studies] |
| [3] | Observational | Moderate | [Result] | [Large cohort N=YYYY] |
| [4] | Systematic Review | Strong | [Synthesis] | [Rigorous protocol] |

## Consensus Meter Output Format

```
┌─────────────────────────────────────────────────┐
│         CONSENSUS METER                         │
│  Question: [Binary Yes/No question]             │
├─────────────────────────────────────────────────┤
│  YES     ██████████████████░░░░░░░  57%  (8)   │
│  POSSIBLY ███░░░░░░░░░░░░░░░░░░░░░   7%  (1)   │
│  MIXED   ████████████░░░░░░░░░░░░░  36%  (5)   │
│  NO      ░░░░░░░░░░░░░░░░░░░░░░░░░   0%  (0)   │
├─────────────────────────────────────────────────┤
│  Total Papers Analyzed: 14                      │
│  Confidence: 100% (≥10 papers)                  │
└─────────────────────────────────────────────────┘
```
