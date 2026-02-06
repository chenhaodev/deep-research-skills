---
name: deep-research
description: |
  Automated systematic literature review agent with consensus analysis.
  
  **Triggers**: systematic review, literature review, consensus analysis, gap analysis, research methodology, academic research
version: 1.0.0
author: OpenCode Community
license: MIT
tags:
  - academic-research
  - literature-review
  - systematic-review
  - consensus-analysis
  - research-methodology
---

## Overview
The Deep Research skill transforms the arduous process of systematic literature reviews into an automated, agentic workflow. It leverages advanced search strategies and consensus analysis to synthesize evidence from academic sources. By automating the retrieval, screening, and synthesis of literature, it allows researchers to focus on high-level interpretation and strategy.

This skill is designed to handle complex research queries, performing multi-angle searches (often 20+ queries) to ensure comprehensive coverage. It quantifies consensus on specific research questions, identifies gaps in the current body of knowledge, and classifies studies based on their methodology (e.g., RCT, Meta-Analysis).

## Trigger Phrases
Use this skill when the user asks to:
- "Conduct a systematic review on..."
- "Perform a literature review regarding..."
- "Analyze the consensus on..."
- "Identify research gaps in..."
- "Synthesize evidence for..."
- "Evaluate the state of research on..."

## Workflow
The agent follows a rigorous 9-step workflow derived from best practices in systematic reviews:

1.  **Initial Survey**: Broad scan to understand the landscape and identify key terms.
2.  **Strategy Formulation**: Defining search terms, databases, and inclusion/exclusion criteria.
3.  **Multi-angle Search**: Executing 20+ diverse queries to maximize recall and minimize bias.
4.  **Citation Graph Expansion**: Traversing references (snowballing) to find connected works.
5.  **Screening**: Filtering results based on relevance, quality, and study design.
6.  **Study Classification**: Categorizing papers (RCT, Meta-Analysis, Case Study, etc.).
7.  **Consensus Quantification**: Statistical analysis of Yes/No questions across studies to determine agreement.
8.  **Gap Analysis**: Creating a matrix of themes vs. technologies/methods to spot missing research.
9.  **Synthesis**: Generating a final report with evidence ratings (Strong/Moderate) and summaries.

## Usage Examples

### Example 1: Medical Research
**User**: "Conduct a systematic review on the efficacy of intermittent fasting for type 2 diabetes remission."
**Action**: The agent performs a multi-angle search, screens clinical trials, quantifies consensus on remission rates, and synthesizes evidence quality.

### Example 2: Software Engineering
**User**: "Analyze the consensus on the impact of remote work on software developer productivity."
**Action**: The agent surveys literature, classifies studies by methodology (surveys vs. metric analysis), and identifies gaps in long-term productivity data.

### Example 3: Emerging Tech
**User**: "Identify research gaps in the application of reinforcement learning to autonomous vehicle safety."
**Action**: The agent maps existing studies to a gap analysis matrix, highlighting under-explored safety scenarios or algorithm types.

## References
For detailed methodologies and protocols, refer to the following documents in the `references/` subdirectory:
- [Literature Search Strategy](references/literature-search.md)
- [Screening Protocol](references/screening-protocol.md)
- [Synthesis Methods](references/synthesis-methods.md)
- [Consensus Analysis](references/consensus-analysis.md)
