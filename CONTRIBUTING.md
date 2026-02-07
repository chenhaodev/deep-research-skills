# Contributing to Deep Research Agent-Skill

Thank you for your interest in contributing! This document provides guidelines for development.

## Development Setup

### Prerequisites
- Python 3.11+
- Git
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/deep-research-skills.git
cd deep-research-skills

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e .
pip install pytest pytest-asyncio pytest-mock pytest-cov responses respx

# Verify installation
pytest tests/ -v
```

## Code Style

### Follow Existing Patterns
This project uses consistent patterns throughout:

- **Async/await everywhere**: All I/O operations are async
- **Type hints**: Use for function signatures
- **Pydantic models**: For data validation
- **Descriptive names**: Functions/classes should be self-documenting

### Formatting
- Line length: 100 characters max
- Use Black formatter settings (configured in pyproject.toml)
- 4-space indentation

### Imports
```python
# Standard library
import asyncio
from pathlib import Path

# Third-party
import httpx
from pydantic import BaseModel

# Local
from deep_research.config import Config
from deep_research.utils.logging import get_logger
```

## Testing Guidelines

### TDD Workflow (RED-GREEN-REFACTOR)

**Always write tests first:**

1. **RED**: Write a failing test
```python
# tests/test_new_feature.py
def test_new_feature():
    result = new_function()
    assert result == expected
```

2. **GREEN**: Implement minimum code to pass
```python
# deep_research/module.py
def new_function():
    return expected  # Minimal implementation
```

3. **REFACTOR**: Clean up while keeping tests green

### Test Structure
```python
import pytest
from deep_research.module import MyClass

@pytest.fixture
def my_fixture():
    return MyClass()

def test_basic_functionality(my_fixture):
    """Test description"""
    result = my_fixture.method()
    assert result is not None

@pytest.mark.asyncio
async def test_async_function():
    """Async test"""
    result = await async_function()
    assert result == expected
```

### Coverage Requirements
- Minimum 80% coverage for new code
- All public APIs must be tested
- Critical algorithms (consensus, gap analysis) need 100% coverage

### Running Tests
```bash
# All tests
pytest tests/ -v

# Specific file
pytest tests/test_search.py -v

# With coverage
pytest tests/ -v --cov=deep_research --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Architecture Guidelines

### Module Organization

```
deep_research/
├── api/          # External API clients (Qwen, Semantic Scholar, PubMed)
├── core/         # Core research engines (search, screening, synthesis)
├── storage/      # Data persistence (SQLite caching)
├── utils/        # Utilities (logging, rate limiting, fetching)
├── cli/          # CLI interface (minimal - OpenCode TUI is primary)
└── config.py     # Configuration management
```

### Adding a New API Client

1. Create `deep_research/api/new_client.py`:
```python
class NewClient:
    def __init__(self, api_key: str):
        self.client = httpx.AsyncClient(timeout=30)
    
    async def fetch_data(self, query: str):
        # Implementation
        pass
```

2. Add tests in `tests/test_new_client.py`
3. Mock HTTP calls with `respx`
4. Document in README

### Adding a New Core Engine

1. Create `deep_research/core/new_engine.py`
2. Follow existing patterns (async, logging, type hints)
3. Add comprehensive tests
4. Update orchestrator if needed
5. Document algorithm in `.opencode/skills/deep-research/references/`

## Reference Documentation

All algorithms are specified in `.opencode/skills/deep-research/references/`:

- `literature-search.md` - Search strategies and query patterns
- `screening-protocol.md` - Deduplication, quality, and relevance rules
- `synthesis-methods.md` - Evidence rating and study classification
- `consensus-analysis.md` - Consensus quantification and gap analysis algorithms

**IMPORTANT:** When implementing features, follow the **EXACT** algorithms in these docs.

## Commit Guidelines

### Commit Message Format
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `test`: Adding tests
- `refactor`: Code refactoring
- `perf`: Performance improvement
- `chore`: Maintenance

**Examples:**
```
feat(search): add multi-angle query generation with LLM

Implements 6-angle search strategy using Qwen3 Max:
- Bottlenecks, whitespace, scenarios, terminology, international, foundational
- Generates 3-4 queries per angle (20-25 total)
- Uses LLM to extract synonyms from survey results

Closes #123
```

```
fix(consensus): correct confidence calculation for edge case

Previously failed when exactly 10 papers. Now correctly returns 1.0.

Fixes #456
```

## Pull Request Process

1. **Fork** the repository
2. **Create branch**: `git checkout -b feature/your-feature-name`
3. **Implement** with tests (TDD)
4. **Verify tests pass**: `pytest tests/ -v`
5. **Check coverage**: Should be ≥80%
6. **Commit** with clear messages
7. **Push**: `git push origin feature/your-feature-name`
8. **Create PR** with description

### PR Description Template
```markdown
## Summary
Brief description of changes

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Documentation
- [ ] Performance improvement

## Testing
- [ ] All tests pass
- [ ] Added new tests
- [ ] Coverage ≥80%

## Checklist
- [ ] Follows code style
- [ ] Added/updated documentation
- [ ] No breaking changes (or documented)
```

## Adding Examples

Examples should be in `examples/` directory:

```python
"""
Example Title - Deep Research Agent-Skill

Brief description of what this example demonstrates.
"""

import asyncio
from deep_research.core.search_orchestrator import SearchOrchestrator
# ... other imports

async def main():
    # Clear, commented code showing usage
    pass

if __name__ == "__main__":
    asyncio.run(main())
```

## Documentation

### Docstrings
Use for public APIs only (not every internal function):

```python
async def quantify_consensus(
    self,
    papers: List[Paper],
    question: str,
    qwen_client: QwenClient
) -> Dict:
    """
    Quantify consensus on a Yes/No research question.
    
    Args:
        papers: Filtered papers to analyze
        question: Yes/No research question
        qwen_client: LLM client for analysis
    
    Returns:
        Dictionary with yes_percent, no_percent, mixed_percent, confidence
    
    Raises:
        ValueError: If fewer than 5 papers provided
    """
```

### README Updates
When adding features, update:
- Features list
- Usage examples
- API Reference
- Configuration options (if applicable)

## Common Issues

### Import Errors
```python
# WRONG
from deep_research.api import models

# CORRECT
from deep_research.api.models import Paper, SearchResult
```

### Async/Await
```python
# WRONG
def fetch_data():
    return httpx.get(url)

# CORRECT
async def fetch_data():
    async with httpx.AsyncClient() as client:
        return await client.get(url)
```

### Mock API Calls in Tests
```python
import respx
import httpx

@pytest.mark.asyncio
@respx.mock
async def test_api_call():
    respx.get("https://api.example.com/data").mock(
        return_value=httpx.Response(200, json={"result": "success"})
    )
    
    # Test code that calls the API
    result = await my_function()
    assert result == "success"
```

## Questions?

- Open an issue on GitHub
- Check existing documentation in `.opencode/skills/deep-research/`
- Review `CHECKPOINT.md` for implementation details

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
