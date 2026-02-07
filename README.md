# Deep Research Agent-Skill

**Automated systematic literature review with consensus quantification and gap analysis**

[![Tests](https://img.shields.io/badge/tests-48%20passing-brightgreen)]()
[![Coverage](https://img.shields.io/badge/coverage-91%25-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.11+-blue)]()
[![License](https://img.shields.io/badge/license-MIT-blue)]()

An OpenCode agent-skill that performs automated systematic literature reviews using LLM-powered multi-angle search, rigorous screening, consensus quantification, and research gap analysis.

## ✨ Features

### Core Capabilities
- **Multi-Angle Search Strategy**: Executes 20-25 queries across 6 angles (bottlenecks, whitespace, scenarios, terminology, international, foundational)
- **Citation Graph Exploration**: 2-level forward/backward citation traversal to find foundational work
- **Rigorous Screening Funnel**: Deduplication → Quality filtering → Semantic relevance scoring
- **Consensus Quantification**: Statistical analysis of Yes/No research questions with confidence metrics
- **Gap Analysis Matrix**: 5×5 themes × technologies matrix identifying research opportunities
- **Evidence Synthesis**: Strong/Moderate ratings, study classification (RCT, Meta-Analysis, etc.)
- **Markdown Report Generation**: Publication-ready reports with inline citations

### Technical Highlights
- Async/parallel API execution for performance
- SQLite caching with TTL (30-day default)
- 91% test coverage with TDD workflow
- Sentence-transformers for semantic similarity
- OpenAI-compatible Qwen3 Max LLM integration

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/deep-research-skills.git
cd deep-research-skills

# Install the package
pip install -e .

# Or install with dependencies
pip install -r requirements.txt
```

### Configuration

Create `~/.deep-research/config.yaml`:

```yaml
qwen:
  api_key: YOUR_QWEN_API_KEY  # Get from OpenRouter or Novita AI
  base_url: "https://openrouter.ai/api/v1"
  model: "qwen/qwen3-max"

cache:
  enabled: true
  ttl_days: 30

search:
  max_papers_per_query: 100
  relevance_threshold: 0.6
```

Or use environment variables:
```bash
export DEEP_RESEARCH_QWEN_API_KEY="your_key_here"
```

### Usage with OpenCode (Recommended)

This skill is designed for OpenCode's TUI:

```
# In OpenCode:
"Run a systematic review on telemedicine effectiveness using deep-research"
```

The skill will automatically:
1. Execute multi-angle search across Semantic Scholar + PubMed
2. Screen papers through rigorous funnel
3. Quantify consensus and identify gaps
4. Generate markdown report with citations

### Usage as Python Package

```python
import asyncio
from deep_research.core.search_orchestrator import SearchOrchestrator
from deep_research.core.screening import ScreeningPipeline
from deep_research.core.synthesis_orchestrator import SynthesisOrchestrator
from deep_research.api.qwen import QwenClient
from deep_research.api.semantic_scholar import SemanticScholarClient
from deep_research.api.pubmed import PubMedClient
from deep_research.config import Config

async def main():
    # Initialize
    config = Config()
    qwen = QwenClient(config.qwen)
    ss = SemanticScholarClient()
    pubmed = PubMedClient()
    
    query = "AI in healthcare diagnosis"
    
    # Search
    search_orch = SearchOrchestrator(qwen, ss, pubmed)
    papers = await search_orch.run_full_search(query)
    print(f"Found {len(papers.papers)} papers")
    
    # Screen
    pipeline = ScreeningPipeline(config)
    filtered = await pipeline.run_screening(papers.papers, query, config)
    print(f"Filtered to {len(filtered)} relevant papers")
    
    # Synthesize
    synth = SynthesisOrchestrator(qwen)
    results = await synth.synthesize(filtered, query, qwen)
    
    # Access results
    print("\n=== CONSENSUS ===")
    print(f"Question: {results['consensus']['question']}")
    print(f"YES: {results['consensus']['yes_percent']}%")
    print(f"Confidence: {results['consensus']['confidence']}")
    
    print("\n=== GAPS ===")
    gaps = results['gaps']
    print(f"Themes: {gaps['themes']}")
    print(f"Technologies: {gaps['technologies']}")
    print(f"Research Opportunities: {len(gaps['gaps'])}")
    
    print("\n=== REPORT ===")
    with open("report.md", "w") as f:
        f.write(results['report'])
    print("Saved to report.md")

asyncio.run(main())
```

## 📊 Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                    SEARCH PHASE                             │
│  Multi-Angle Strategy → Citation Graph → Deduplication     │
│  (20-25 queries across 6 angles + 2-level citation graph)  │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│                  SCREENING PHASE                            │
│  Deduplication → Quality Filter → Relevance Scoring        │
│  (Funnel: e.g., 948 → 589 → 359 → 149 papers)             │
└──────────────────────┬──────────────────────────────────────┘
                       ↓
┌─────────────────────────────────────────────────────────────┐
│                 SYNTHESIS PHASE                             │
│  Evidence Extraction → Study Classification →              │
│  Consensus Quantification → Gap Analysis → Report          │
└─────────────────────────────────────────────────────────────┘
```

## 🎯 Core Algorithms

### Multi-Angle Search (6 Angles)
1. **Bottlenecks**: `{query} AND (limitation OR bottleneck OR challenge)`
2. **Whitespace**: `{query} AND (gap OR unexplored OR future research)`
3. **Scenarios**: `{query} AND (application OR use case OR implementation)`
4. **Terminology**: Synonyms extracted from survey results
5. **International**: `{query} AND (country OR regional OR international)`
6. **Foundational**: `{query} AND (review OR survey OR foundational)`

### Consensus Quantification (5 Steps)
1. Filter papers addressing the question (LLM: "Does this paper answer: {question}?")
2. Extract conclusion (LLM: "What is this paper's answer? YES/NO/MIXED/POSSIBLY")
3. Calculate percentages: `(count / total) × 100`
4. Compute confidence: `min(1.0, n_papers / 10)` (≥10 papers = 100%)
5. Validate: Error if n_papers < 5

### Gap Analysis Matrix (5 Steps)
1. Extract themes (LLM: "Top 5 themes/scenarios?")
2. Extract technologies (LLM: "Top 5 technologies/methods?")
3. Build 5×5 matrix: Check if papers cover (theme, technology) intersections
4. Mark cells with 0 papers as "GAP"
5. Generate opportunities (LLM: "Given these gaps, what research opportunities exist?")

## 📚 Examples

See the `examples/` directory:

- `basic_search.py` - Simple search and screen workflow
- `consensus_analysis.py` - Quantifying consensus on research questions
- `gap_analysis.py` - Identifying research gaps

## 🏗️ Architecture

```
deep_research/
├── api/              # API clients (Qwen, Semantic Scholar, PubMed)
├── core/             # Research engines
│   ├── survey.py                    # Initial search
│   ├── strategy.py                  # Multi-angle planning
│   ├── search_orchestrator.py       # Search workflow
│   ├── screening.py                 # Screening pipeline
│   ├── consensus.py                 # Consensus analysis
│   ├── gap_analysis.py              # Gap identification
│   └── synthesis_orchestrator.py    # Synthesis workflow
├── storage/          # SQLite caching
├── utils/            # Utilities (logging, rate limiting, fetching)
└── config.py         # Configuration management
```

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# With coverage
pytest tests/ -v --cov=deep_research

# Expected: 48 tests, 91% coverage
```

## 📖 API Reference

### SearchOrchestrator

```python
orchestrator = SearchOrchestrator(qwen_client, ss_client, pubmed_client)
result = await orchestrator.run_full_search(query: str) -> SearchResult
```

### ScreeningPipeline

```python
pipeline = ScreeningPipeline(config)
filtered = await pipeline.run_screening(
    papers: List[Paper],
    query: str,
    config: SearchConfig
) -> List[Paper]
```

### SynthesisOrchestrator

```python
orchestrator = SynthesisOrchestrator(qwen_client)
results = await orchestrator.synthesize(
    papers: List[Paper],
    query: str,
    qwen_client: QwenClient
) -> Dict
```

Returns:
```python
{
    "evidence": List[Dict],      # Extracted evidence with ratings
    "classifications": List[Dict],  # Study types + badges
    "consensus": {
        "question": str,
        "yes_percent": float,
        "no_percent": float,
        "mixed_percent": float,
        "confidence": float
    },
    "gaps": {
        "themes": List[str],
        "technologies": List[str],
        "matrix": List[List[int]],
        "gaps": List[Dict]
    },
    "report": str  # Markdown report
}
```

## 🔧 Configuration Options

| Setting | Default | Description |
|---------|---------|-------------|
| `qwen.model` | qwen/qwen3-max | LLM model for analysis |
| `cache.ttl_days` | 30 | Cache expiration in days |
| `cache.enabled` | true | Enable/disable caching |
| `search.max_papers_per_query` | 100 | Papers per query |
| `search.max_searches_per_review` | 25 | Total queries per review |
| `search.relevance_threshold` | 0.6 | Minimum relevance score (0-1) |
| `search.min_abstract_words` | 50 | Minimum abstract length |
| `search.date_range_years` | 3 | Search papers from last N years |

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines.

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- Built for [OpenCode](https://github.com/opencode-ai)
- Powered by [Qwen3 Max](https://openrouter.ai/qwen/qwen3-max)
- Uses [Semantic Scholar API](https://www.semanticscholar.org/product/api)
- Uses [PubMed E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/)
- Embeddings by [sentence-transformers](https://www.sbert.net/)

## 📬 Support

For issues and questions:
- GitHub Issues: [Report a bug](https://github.com/YOUR_USERNAME/deep-research-skills/issues)
- Documentation: See `.opencode/skills/deep-research/` for detailed SOPs

---

**Built with ULTRAWORK MODE** - Production-ready academic research automation for OpenCode.
