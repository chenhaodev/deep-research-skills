import httpx
from typing import List, Optional
from deep_research.api.models import Paper, SearchResult, Author, ExternalIds
from deep_research.utils.logging import get_logger

logger = get_logger(__name__)


class SemanticScholarClient:
    BASE_URL = "https://api.semanticscholar.org/graph/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.client = httpx.AsyncClient(timeout=30)
    
    def _get_headers(self):
        headers = {}
        if self.api_key:
            headers["x-api-key"] = self.api_key
        return headers
    
    def _parse_paper(self, data: dict) -> Paper:
        authors = [Author(name=a.get("name", ""), author_id=a.get("authorId")) 
                   for a in data.get("authors", [])]
        
        external_ids = ExternalIds(
            doi=data.get("externalIds", {}).get("DOI"),
            pmid=data.get("externalIds", {}).get("PubMed"),
            arxiv=data.get("externalIds", {}).get("ArXiv"),
            s2_id=data.get("paperId")
        )
        
        return Paper(
            paper_id=data.get("paperId", ""),
            title=data.get("title", ""),
            abstract=data.get("abstract"),
            year=data.get("year"),
            authors=authors,
            venue=data.get("venue"),
            citation_count=data.get("citationCount", 0),
            reference_count=data.get("referenceCount", 0),
            external_ids=external_ids,
            url=data.get("url"),
            publication_types=data.get("publicationTypes", []),
            publication_date=data.get("publicationDate")
        )
    
    async def search_papers(
        self,
        query: str,
        limit: int = 100,
        offset: int = 0,
        fields: Optional[str] = None
    ) -> SearchResult:
        if fields is None:
            fields = "paperId,title,abstract,year,authors,venue,citationCount,externalIds,url,publicationTypes"
        
        url = f"{self.BASE_URL}/paper/search"
        params = {
            "query": query,
            "limit": min(limit, 100),
            "offset": offset,
            "fields": fields
        }
        
        response = await self.client.get(url, params=params, headers=self._get_headers())
        
        if response.status_code == 404:
            raise Exception(f"Paper not found (404)")
        
        response.raise_for_status()
        data = response.json()
        
        papers = [self._parse_paper(p) for p in data.get("data", [])]
        return SearchResult(papers=papers, total=data.get("total", 0), offset=offset)
    
    async def get_paper(self, paper_id: str, fields: Optional[str] = None) -> Paper:
        if fields is None:
            fields = "paperId,title,abstract,year,authors,venue,citationCount,externalIds,url"
        
        url = f"{self.BASE_URL}/paper/{paper_id}"
        params = {"fields": fields}
        
        response = await self.client.get(url, params=params, headers=self._get_headers())
        
        if response.status_code == 404:
            raise Exception(f"Paper not found (404)")
        
        response.raise_for_status()
        return self._parse_paper(response.json())
    
    async def get_citations(self, paper_id: str, limit: int = 100) -> List[Paper]:
        url = f"{self.BASE_URL}/paper/{paper_id}/citations"
        params = {
            "limit": min(limit, 100),
            "fields": "paperId,title,year,citationCount"
        }
        
        response = await self.client.get(url, params=params, headers=self._get_headers())
        response.raise_for_status()
        
        data = response.json()
        return [self._parse_paper(item["citingPaper"]) for item in data.get("data", [])]
    
    async def get_references(self, paper_id: str, limit: int = 100) -> List[Paper]:
        url = f"{self.BASE_URL}/paper/{paper_id}/references"
        params = {
            "limit": min(limit, 100),
            "fields": "paperId,title,year,citationCount"
        }
        
        response = await self.client.get(url, params=params, headers=self._get_headers())
        response.raise_for_status()
        
        data = response.json()
        return [self._parse_paper(item["citedPaper"]) for item in data.get("data", [])]
    
    async def close(self):
        await self.client.aclose()
