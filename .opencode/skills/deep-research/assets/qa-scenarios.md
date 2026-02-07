# QA Scenarios - Deep Research Agent-Skill

Real-world test scenarios demonstrating expected skill behavior.

---

## Scenario 1: Systematic Review on Emerging Technology

**User Request:**
> "Run a systematic review on blockchain in healthcare supply chain management"

**Expected Behavior:**
1. **Search Phase:**
   - Executes 6-angle search strategy:
     - Bottlenecks: "blockchain healthcare supply chain AND (limitation OR challenge)"
     - Whitespace: "blockchain healthcare supply chain AND (gap OR future research)"
     - Scenarios: "blockchain healthcare supply chain AND (application OR use case)"
     - Terminology: Extracts synonyms (e.g., "distributed ledger", "DLT")
     - International: "blockchain healthcare supply chain AND (country OR regional)"
     - Foundational: "blockchain healthcare supply chain AND (review OR survey)"
   - Executes ~20-25 total queries
   - Explores citation graph (2 levels)
   - Returns 200-500 papers

2. **Screening Phase:**
   - Deduplicates by DOI/PMID
   - Filters by quality (has abstract, ≥50 words, last 3 years)
   - Scores semantic relevance (threshold 0.6)
   - Funnel: e.g., 400 → 280 dedup → 180 quality → 80 relevant

3. **Synthesis Phase:**
   - Classifies studies (observational, case study, review)
   - Rates evidence strength (moderate for most, strong for reviews)
   - Identifies gaps in 5×5 matrix
   - Generates markdown report with citations

**Success Criteria:**
- All 6 search angles executed
- Screening funnel logs metrics at each stage
- Final report contains consensus meter and gap analysis table
- Report has ≥20 inline citations

---

## Scenario 2: Consensus Analysis on Clinical Question

**User Request:**
> "What is the consensus on whether AI can improve diagnostic accuracy compared to radiologists?"

**Expected Behavior:**
1. **Search:** Query "AI diagnostic accuracy radiology"
2. **Screen:** Filter to RCTs and meta-analyses
3. **Consensus Analysis:**
   - Filter papers addressing Yes/No question
   - Extract conclusions (YES/NO/MIXED)
   - Calculate: YES: 62%, NO: 8%, MIXED: 30% (example)
   - Confidence: 1.0 (if ≥10 papers)
4. **Output:**
   - Consensus meter visualization
   - Statistical breakdown
   - Confidence score

**Success Criteria:**
- Consensus percentages sum to 100%
- Confidence correctly calculated (n_papers / 10, max 1.0)
- Error if <5 papers found
- Report cites specific papers for each category

---

## Scenario 3: Gap Analysis for Research Planning

**User Request:**
> "Identify research gaps in remote patient monitoring for elderly care"

**Expected Behavior:**
1. **Search:** Multi-angle strategy on "remote patient monitoring elderly care"
2. **Screen:** Recent papers (last 3 years), high relevance
3. **Gap Analysis:**
   - Extract 5 themes (e.g., "Fall Detection", "Medication Adherence", "Vital Signs", "Social Isolation", "Cognitive Decline")
   - Extract 5 technologies (e.g., "Wearables", "IoT Sensors", "ML Algorithms", "Mobile Apps", "Voice Assistants")
   - Build 5×5 matrix
   - Identify cells with 0 papers (GAPs)
   - Generate research opportunities
4. **Output:**
   - Matrix table showing paper counts
   - List of gaps with opportunity descriptions
   - Ranked by potential impact

**Success Criteria:**
- Matrix is exactly 5×5
- At least 3 gaps identified (realistic for any domain)
- Opportunities are actionable and specific
- Report includes both matrix and gap descriptions

---

## Scenario 4: Evidence Synthesis with Quality Assessment

**User Request:**
> "Synthesize evidence on effectiveness of cognitive behavioral therapy for insomnia"

**Expected Behavior:**
1. **Search:** "cognitive behavioral therapy insomnia effectiveness"
2. **Screen:** Focus on RCTs and systematic reviews
3. **Evidence Extraction:**
   - Extract 1-3 key claims per paper
   - Rate evidence:
     - Strong: RCTs with ≥100 citations, meta-analyses
     - Moderate: RCTs with 50-99 citations, observational
4. **Study Classification:**
   - Detect RCTs via keywords ("randomized controlled trial")
   - Detect meta-analyses
   - Add badges: [RCT], [Highly Cited], [Rigorous Journal]
5. **Output:**
   - Evidence table with strength ratings
   - Study classifications
   - Quality badges

**Success Criteria:**
- All papers classified correctly by type
- Evidence strength follows exact rules from synthesis-methods.md
- Quality badges assigned correctly (>100 citations = Highly Cited)
- Report separates Strong vs Moderate evidence sections

---

## Scenario 5: Multi-Language Query (English Only for v1.0)

**User Request:**
> "Recherche systématique sur l'IA en santé" (French: systematic review on AI in healthcare)

**Expected Behavior:**
1. **Language Detection:** Detects non-English query
2. **Response:** "Please provide your query in English. I currently support English-language papers only."
3. **Alternative:** User re-phrases in English: "systematic review on AI in healthcare"
4. **Proceed:** Normal workflow

**Success Criteria:**
- Polite error message for non-English
- Clear guidance to rephrase
- Works normally with English query

---

## Scenario 6: Low Volume Topic (Few Papers Found)

**User Request:**
> "Consensus on quantum computing applications in genomic sequencing"

**Expected Behavior:**
1. **Search:** Executes multi-angle search
2. **Screen:** Finds only 8 papers after filtering
3. **Consensus Analysis:**
   - Attempts consensus quantification
   - Detects n_papers < 10
   - Returns consensus results with LOW CONFIDENCE warning
4. **Output:**
   - Consensus percentages (based on 8 papers)
   - Confidence: 0.8 (8 / 10)
   - Warning: "⚠️ Low confidence due to limited papers (N=8). Need ≥10 for 100% confidence."

**Success Criteria:**
- Does not error (minimum is 5 papers)
- Confidence correctly calculated: 0.8
- Warning displayed prominently
- User understands limitation

---

## Scenario 7: High Volume Topic (Many Papers)

**User Request:**
> "Systematic review on deep learning for image classification"

**Expected Behavior:**
1. **Search:** Finds 1000+ papers in initial survey
2. **Screening:**
   - Deduplication: 1000 → 750
   - Quality: 750 → 600
   - Relevance: 600 → 200 (strict threshold 0.6)
3. **Synthesis:**
   - Processes top 200 papers (manageable for LLM)
   - Groups by sub-themes (medical, satellite, industrial)
   - Generates comprehensive report

**Success Criteria:**
- Handles large volume without errors
- Screening reduces to manageable size
- Report well-structured with sub-sections
- Processing time <10 minutes (with caching)

---

## Scenario 8: Caching Behavior

**User Request:**
> "Run systematic review on telemedicine effectiveness" (repeated query)

**Expected Behavior:**
1. **First Run:**
   - API calls to Semantic Scholar + PubMed
   - Stores all papers in SQLite cache
   - Processing time: ~5-7 minutes
2. **Second Run (same query, <30 days later):**
   - Cache hits for most papers
   - Reduced API calls
   - Processing time: ~2-3 minutes (60% faster)
3. **Second Run (>30 days later):**
   - Cache expired (TTL exceeded)
   - Fresh API calls
   - Processing time: ~5-7 minutes (same as first)

**Success Criteria:**
- Cache correctly stores and retrieves papers
- TTL expiration works (30-day default)
- Logs show cache hits: "Cache HIT: paper_id"
- Performance improvement measurable

---

## Scenario 9: Error Handling - Invalid API Key

**User Request:**
> "Run systematic review on cloud computing security"

**System State:** Invalid or missing Qwen API key

**Expected Behavior:**
1. **Initialization:** Attempts to create QwenClient
2. **First API Call:** 401 Unauthorized error
3. **Error Handling:**
   - Catches authentication error
   - Returns clear message: "❌ Authentication failed. Please check your Qwen API key in ~/.deep-research/config.yaml or DEEP_RESEARCH_QWEN_API_KEY environment variable."
4. **No Partial Results:** Does not proceed with incomplete data

**Success Criteria:**
- Clear, actionable error message
- Points user to configuration location
- Does not crash or produce partial results
- Suggests environment variable alternative

---

## Scenario 10: Integration Test - Full Workflow

**User Request:**
> "Complete systematic review on wearable sensors for fall detection in elderly care, including consensus on effectiveness and gap analysis"

**Expected Behavior:**
1. **Search Phase (2-3 min):**
   - 20-25 queries across 6 angles
   - Citation graph exploration
   - ~300-500 papers found
2. **Screening Phase (1 min):**
   - Funnel: 400 → 280 → 200 → 120 papers
3. **Synthesis Phase (3-4 min):**
   - Evidence extraction: 120 papers → 250 claims
   - Study classification: 40 RCTs, 30 Observational, 20 Reviews
   - Consensus: "Is wearable fall detection effective?" → YES: 68%, MIXED: 25%, NO: 7%
   - Gap analysis: 5×5 matrix with 8 gaps identified
4. **Report Generation (<1 min):**
   - 5000+ word markdown report
   - 50+ inline citations
   - Consensus meter visualization
   - Gap matrix table
   - Bibliography with DOIs

**Success Criteria:**
- Total processing time <10 minutes
- All components execute successfully
- Report is publication-ready
- No errors or warnings
- All 48 tests pass in test suite

**Verification:**
```bash
pytest tests/ -v
# Expected: 48 passed, 91% coverage
```

---

## Notes for Developers

- **Test Data:** Use `responses` library to mock API calls in tests
- **Reproducibility:** Same query should produce similar results (allowing for API data updates)
- **Performance:** Cache should provide 50-70% speedup on repeated queries
- **Quality:** All algorithms follow exact SOPs in `.opencode/skills/deep-research/references/`
