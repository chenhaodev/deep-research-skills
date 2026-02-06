import pytest
import httpx
import respx
from deep_research.api.pubmed import PubMedClient


@pytest.mark.asyncio
@respx.mock
async def test_pubmed_search():
    client = PubMedClient()
    
    respx.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi").mock(
        return_value=httpx.Response(200, json={
            "esearchresult": {
                "idlist": ["12345", "67890"]
            }
        })
    )
    
    pmids = await client.search("machine learning")
    assert len(pmids) == 2
    assert "12345" in pmids


@pytest.mark.asyncio
@respx.mock
async def test_pubmed_fetch_details():
    client = PubMedClient()
    
    xml_response = """<?xml version="1.0"?>
    <PubmedArticleSet>
        <PubmedArticle>
            <MedlineCitation>
                <PMID>12345</PMID>
                <Article>
                    <ArticleTitle>Test Article</ArticleTitle>
                    <Abstract>
                        <AbstractText>Test abstract text</AbstractText>
                    </Abstract>
                    <AuthorList>
                        <Author>
                            <LastName>Smith</LastName>
                            <ForeName>John</ForeName>
                        </Author>
                    </AuthorList>
                </Article>
                <PubDate>
                    <Year>2023</Year>
                </PubDate>
            </MedlineCitation>
        </PubmedArticle>
    </PubmedArticleSet>
    """
    
    respx.get("https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi").mock(
        return_value=httpx.Response(200, text=xml_response)
    )
    
    papers = await client.fetch_details(["12345"])
    assert len(papers) == 1
    assert papers[0].title == "Test Article"
    assert papers[0].abstract == "Test abstract text"
