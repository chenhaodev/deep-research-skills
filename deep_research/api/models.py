from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class Author(BaseModel):
    name: str
    author_id: Optional[str] = None


class ExternalIds(BaseModel):
    doi: Optional[str] = None
    pmid: Optional[str] = None
    arxiv: Optional[str] = None
    s2_id: Optional[str] = None


class Paper(BaseModel):
    paper_id: str
    title: str
    abstract: Optional[str] = None
    year: Optional[int] = None
    authors: List[Author] = Field(default_factory=list)
    venue: Optional[str] = None
    citation_count: int = 0
    reference_count: int = 0
    external_ids: ExternalIds = Field(default_factory=ExternalIds)
    url: Optional[str] = None
    publication_types: List[str] = Field(default_factory=list)
    publication_date: Optional[str] = None
    
    @property
    def has_abstract(self) -> bool:
        return self.abstract is not None and len(self.abstract.strip()) > 0
    
    @property
    def abstract_word_count(self) -> int:
        if not self.has_abstract:
            return 0
        return len(self.abstract.split())


class SearchResult(BaseModel):
    papers: List[Paper]
    total: int
    offset: int = 0


class QwenResponse(BaseModel):
    content: str
    model: str
    usage: Dict[str, int] = Field(default_factory=dict)
