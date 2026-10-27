"""Web Search skill — high-level interface for searching the web via Exa Labs."""

from typing import Any

from .client import ExaClient
from .config import DEFAULT_NUM_RESULTS, DEFAULT_SEARCH_MODE
from .models import (
    ContentsRequest,
    ContentsResponse,
    FindSimilarRequest,
    FindSimilarResponse,
    SearchRequest,
    SearchResponse,
    SearchResult,
)


class WebSearchSkill:
    """Skill that searches the web using the Exa Labs API.

    Provides three operations:
        - search: general web search with filters
        - contents: extract text/highlights/summaries from result IDs
        - find_similar: find pages similar to a seed URL or result ID
    """

    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:
        self.api_key = api_key
        self.base_url = base_url

    async def search(
        self,
        query: str,
        num_results: int = DEFAULT_NUM_RESULTS,
        mode: str = DEFAULT_SEARCH_MODE,
        domains: list[str] | None = None,
        categories: list[str] | None = None,
        start_published_date: str | None = None,
        end_published_date: str | None = None,
        include_domains: list[str] | None = None,
        exclude_domains: list[str] | None = None,
    ) -> SearchResponse:
        """Search the web and return structured results."""
        request = SearchRequest(
            query=query,
            num_results=num_results,
            mode=mode,
            domains=domains,
            categories=categories,
            start_published_date=start_published_date,
            end_published_date=end_published_date,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
        )

        async with ExaClient(api_key=self.api_key, base_url=self.base_url) as client:
            data = await client.search(
                query=request.query,
                num_results=request.num_results,
                mode=request.mode,
                domains=request.domains,
                categories=request.categories,
                start_published_date=request.start_published_date,
                end_published_date=request.end_published_date,
                include_domains=request.include_domains,
                exclude_domains=request.exclude_domains,
            )

        results = [
            SearchResult(
                title=item.get("title", ""),
                url=item.get("url", ""),
                score=item.get("score"),
                published_date=item.get("publishedDate"),
                author=item.get("author"),
                image=item.get("image"),
                snippet=item.get("snippet"),
            )
            for item in data.get("results", [])
        ]

        return SearchResponse(
            query=request.query,
            results=results,
            total_results=len(results),
            mode=request.mode,
            raw=data,
        )

    async def contents(
        self,
        ids: list[str],
        text: bool = True,
        highlights: bool = False,
        summaries: bool = False,
    ) -> ContentsResponse:
        """Extract contents (text, highlights, summaries) for given result IDs."""
        request = ContentsRequest(
            ids=ids,
            text=text,
            highlights=highlights,
            summaries=summaries,
        )

        async with ExaClient(api_key=self.api_key, base_url=self.base_url) as client:
            data = await client.contents(
                ids=request.ids,
                text=request.text,
                highlights=request.highlights,
                summaries=request.summaries,
            )

        return ContentsResponse(
            results=data.get("results", []),
            raw=data,
        )

    async def find_similar(
        self,
        url: str | None = None,
        result_id: str | None = None,
        num_results: int = DEFAULT_NUM_RESULTS,
    ) -> FindSimilarResponse:
        """Find pages similar to a seed URL or result ID."""
        request = FindSimilarRequest(
            url=url,
            result_id=result_id,
            num_results=num_results,
        )

        async with ExaClient(api_key=self.api_key, base_url=self.base_url) as client:
            data = await client.find_similar(
                url=request.url,
                result_id=request.result_id,
                num_results=request.num_results,
            )

        results = [
            SearchResult(
                title=item.get("title", ""),
                url=item.get("url", ""),
                score=item.get("score"),
                published_date=item.get("publishedDate"),
                author=item.get("author"),
                image=item.get("image"),
                snippet=item.get("snippet"),
            )
            for item in data.get("results", [])
        ]

        return FindSimilarResponse(
            results=results,
            total_results=len(results),
            raw=data,
        )