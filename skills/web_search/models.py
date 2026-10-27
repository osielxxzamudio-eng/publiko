"""Data models for the Web Search skill requests and responses."""

from typing import Any, Optional
from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    """Request model for the Exa search endpoint."""

    query: str = Field(..., description="Search query string")
    num_results: int = Field(default=10, ge=1, le=100, description="Number of results to return")
    mode: str = Field(default="auto", description="Search mode: neural, keyword, or auto")
    domains: Optional[list[str]] = Field(default=None, description="List of domains to restrict search to")
    categories: Optional[list[str]] = Field(default=None, description="List of content categories")
    start_published_date: Optional[str] = Field(default=None, description="Start date filter (ISO format)")
    end_published_date: Optional[str] = Field(default=None, description="End date filter (ISO format)")
    include_domains: Optional[list[str]] = Field(default=None, description="Domains to include")
    exclude_domains: Optional[list[str]] = Field(default=None, description="Domains to exclude")


class SearchResult(BaseModel):
    """A single search result item."""

    title: str
    url: str
    score: Optional[float] = None
    published_date: Optional[str] = None
    author: Optional[str] = None
    image: Optional[str] = None
    snippet: Optional[str] = None


class SearchResponse(BaseModel):
    """Response model for the Exa search endpoint."""

    query: str
    results: list[SearchResult]
    total_results: int
    mode: str
    raw: dict[str, Any] = Field(default_factory=dict)


class ContentsRequest(BaseModel):
    """Request model for the Exa contents endpoint."""

    ids: list[str] = Field(..., description="List of result IDs to extract contents from")
    text: bool = Field(default=True, description="Extract full text")
    highlights: bool = Field(default=False, description="Extract highlights")
    summaries: bool = Field(default=False, description="Extract summaries")


class ContentsResponse(BaseModel):
    """Response model for the Exa contents endpoint."""

    results: list[dict[str, Any]]
    raw: dict[str, Any] = Field(default_factory=dict)


class FindSimilarRequest(BaseModel):
    """Request model for the Exa find-similar endpoint."""

    url: Optional[str] = Field(default=None, description="Seed URL to find similar content to")
    result_id: Optional[str] = Field(default=None, description="Seed result ID to find similar content to")
    num_results: int = Field(default=10, ge=1, le=100, description="Number of similar results to return")


class FindSimilarResponse(BaseModel):
    """Response model for the Exa find-similar endpoint."""

    results: list[SearchResult]
    total_results: int
    raw: dict[str, Any] = Field(default_factory=dict)