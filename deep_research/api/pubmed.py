import httpx
import xml.etree.ElementTree as ET
from typing import List
from deep_research.api.models import Paper, Author, ExternalIds
from deep_research.utils.logging import get_logger

logger = get_logger(__name__)


class PubMedClient:
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
    
    def __init__(self, api_key: str = "", email: str = ""):
        self.api_key = api_key
        self.email = email
        self.client = httpx.AsyncClient(timeout=30)
    
    async def search(self, query: str, max_results: int = 100) -> List[str]:
        url = f"{self.BASE_URL}/esearch.fcgi"
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json",
            "email": self.email
        }
        if self.api_key:
            params["api_key"] = self.api_key
        
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        
        data = response.json()
        return data.get("esearchresult", {}).get("idlist", [])
    
    async def fetch_details(self, pmids: List[str]) -> List[Paper]:
        if not pmids:
            return []
        
        url = f"{self.BASE_URL}/efetch.fcgi"
        params = {
            "db": "pubmed",
            "id": ",".join(pmids),
            "retmode": "xml",
            "rettype": "abstract",
            "email": self.email
        }
        if self.api_key:
            params["api_key"] = self.api_key
        
        response = await self.client.get(url, params=params)
        response.raise_for_status()
        
        return self._parse_xml(response.text)
    
    def _parse_xml(self, xml_string: str) -> List[Paper]:
        root = ET.fromstring(xml_string)
        papers = []
        
        for article in root.findall(".//PubmedArticle"):
            try:
                pmid = article.find(".//PMID").text if article.find(".//PMID") is not None else ""
                title_elem = article.find(".//ArticleTitle")
                title = title_elem.text if title_elem is not None else ""
                
                abstract_elem = article.find(".//AbstractText")
                abstract = abstract_elem.text if abstract_elem is not None else None
                
                year_elem = article.find(".//PubDate/Year")
                year = int(year_elem.text) if year_elem is not None else None
                
                authors = []
                for author in article.findall(".//Author"):
                    lastname = author.find("LastName")
                    forename = author.find("ForeName")
                    if lastname is not None:
                        name = f"{forename.text} {lastname.text}" if forename is not None else lastname.text
                        authors.append(Author(name=name))
                
                papers.append(Paper(
                    paper_id=f"PMID:{pmid}",
                    title=title,
                    abstract=abstract,
                    year=year,
                    authors=authors,
                    external_ids=ExternalIds(pmid=pmid)
                ))
            except Exception as e:
                logger.warning(f"Failed to parse PubMed article: {e}")
                continue
        
        return papers
    
    async def close(self):
        await self.client.aclose()
