"""
Consensus Analysis Example - Deep Research Agent-Skill

This example demonstrates consensus quantification on a Yes/No research question.
"""

import asyncio
from deep_research.core.search_orchestrator import SearchOrchestrator
from deep_research.core.screening import ScreeningPipeline
from deep_research.core.consensus import ConsensusAnalyzer
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
    
    # Research question (Yes/No format)
    query = "telemedicine"
    question = "Is telemedicine effective for chronic disease management?"
    
    print(f"🔍 Research Question: {question}\n")
    
    # Search & Screen
    print("📚 Searching literature...")
    search_orch = SearchOrchestrator(qwen, ss, pubmed)
    papers = await search_orch.run_full_search(query)
    
    print("🔬 Screening papers...")
    pipeline = ScreeningPipeline(config)
    filtered = await pipeline.run_screening(papers.papers, query, config)
    print(f"   Analyzed {len(filtered)} papers\n")
    
    # Consensus Analysis
    print("📊 Quantifying consensus...")
    analyzer = ConsensusAnalyzer()
    consensus = await analyzer.quantify_consensus(filtered, question, qwen)
    
    # Display results
    print("\n" + "="*60)
    print("CONSENSUS METER")
    print("="*60)
    print(f"Question: {consensus['question']}\n")
    
    # Visual bar chart
    total = consensus['total_papers']
    for category in ['yes', 'no', 'mixed', 'possibly']:
        percent = consensus[f'{category}_percent']
        count = int(total * percent / 100)
        bar_length = int(percent / 2)  # Scale to 50 chars max
        bar = '█' * bar_length + '░' * (50 - bar_length)
        print(f"{category.upper():10} {bar} {percent:5.1f}% (N={count})")
    
    print(f"\nTotal Papers Analyzed: {total}")
    print(f"Confidence: {consensus['confidence']*100:.0f}%")
    
    if consensus['confidence'] < 1.0:
        print(f"⚠️  Low confidence (need ≥10 papers for 100% confidence)")
    
    print("="*60)


if __name__ == "__main__":
    asyncio.run(main())
