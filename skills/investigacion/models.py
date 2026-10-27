"""Data models for the Investigacion skill requests and responses."""

from typing import Any, Optional
from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    """Request model for academic research searches."""

    topic: str = Field(..., description="Research topic or question")
    num_results: int = Field(default=10, ge=1, le=100, description="Number of results")
    domains: Optional[list[str]] = Field(default=None, description="Academic domains to search")
    categories: Optional[list[str]] = Field(default=None, description="Content categories")
    include_domains: Optional[list[str]] = Field(default=None, description="Domains to include")
    exclude_domains: Optional[list[str]] = Field(default=None, description="Domains to exclude")
    start_published_date: Optional[str] = Field(default=None, description="Start date (ISO)")
    end_published_date: Optional[str] = Field(default=None, description="End date (ISO)")


class ResearchResult(BaseModel):
    """A single research result item."""

    title: str
    url: str
    score: Optional[float] = None
    published_date: Optional[str] = None
    author: Optional[str] = None
    snippet: Optional[str] = None
    source_type: Optional[str] = Field(default=None, description="paper, article, thesis, etc.")


class ResearchResponse(BaseModel):
    """Response model for research searches."""

    topic: str
    results: list[ResearchResult]
    total_results: int
    raw: dict[str, Any] = Field(default_factory=dict)


class MethodologyRequest(BaseModel):
    """Request to search for research methodologies on a topic."""

    topic: str = Field(..., description="Research topic")
    methodology_type: Optional[str] = Field(
        default=None,
        description="qualitative, quantitative, mixed, experimental, case study, etc."
    )
    num_results: int = Field(default=10, ge=1, le=100)


class MethodologyResponse(BaseModel):
    """Response with research methodologies found."""

    topic: str
    methodology_type: Optional[str]
    results: list[ResearchResult]
    total_results: int
    raw: dict[str, Any] = Field(default_factory=dict)


class LiteratureReviewRequest(BaseModel):
    """Request for literature review search."""

    research_question: str = Field(..., description="The research question to investigate")
    key_concepts: Optional[list[str]] = Field(default=None, description="Key concepts to search")
    num_results: int = Field(default=10, ge=1, le=100)


class LiteratureReviewResponse(BaseModel):
    """Response for literature review."""

    research_question: str
    key_concepts: Optional[list[str]]
    results: list[ResearchResult]
    total_results: int
    raw: dict[str, Any] = Field(default_factory=dict)