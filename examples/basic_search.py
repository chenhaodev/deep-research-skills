"""
Basic Search Example - Deep Research Agent-Skill

This example demonstrates a simple search and screening workflow.
"""

import asyncio
from deep_research.core.search_orchestrator import SearchOrchestrator
from deep_research.core.screening import ScreeningPipeline
from deep_research.api.qwen import QwenClient
from deep_research.api.semantic_scholar import SemanticScholarClient
from deep_research.api.pubmed import PubMedClient
from deep_research.storage.cache import CacheManager
from deep_research.config import Config
from pathlib import Path


async def main():
    # Initialize configuration
    config = Config()
    
    # Initialize API clients
    qwen = QwenClient(config.qwen)
    cache = CacheManager(Path.home() / ".deep-research" / "cache.db")
    ss = SemanticScholarClient(cache=cache)
    pubmed = PubMedClient()
    
    # Define research query
    query = "machine learning in medical diagnosis"
    
    print(f"🔍 Starting search for: {query}\n")
    
    # STEP 1: Search
    print("📚 Executing multi-angle search...")
    search_orch = SearchOrchestrator(qwen, ss, pubmed)
    search_results = await search_orch.run_full_search(query)
    print(f"   Found {len(search_results.papers)} papers")
    
    # STEP 2: Screen
    print("\n🔬 Screening papers through funnel...")
    pipeline = ScreeningPipeline(config)
    filtered_papers = await pipeline.run_screening(
        search_results.papers,
        query,
        config
    )
    print(f"   Filtered to {len(filtered_papers)} relevant papers")
    
    # Display sample results
    print("\n📄 Sample Results:")
    for i, paper in enumerate(filtered_papers[:5], 1):
        print(f"\n{i}. {paper.title}")
        print(f"   Authors: {', '.join(a.name for a in paper.authors[:3])}")
        print(f"   Year: {paper.year}")
        print(f"   Citations: {paper.citation_count}")
    
    print(f"\n✅ Complete! Found {len(filtered_papers)} relevant papers.")


if __name__ == "__main__":
    asyncio.run(main())
