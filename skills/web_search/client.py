"""HTTP client for the Exa Labs API."""

from typing import Any

import httpx

from .config import (
    CONTENTS_ENDPOINT,
    EXA_API_BASE_URL,
    EXA_AUTH_HEADER,
    EXA_API_KEY,
    FIND_SIMILAR_ENDPOINT,
    REQUEST_TIMEOUT_SECONDS,
    SEARCH_ENDPOINT,
)


class ExaClient:
    """Async HTTP client for Exa Labs API."""

    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:
        self.api_key = api_key or EXA_API_KEY
        self.base_url = base_url or EXA_API_BASE_URL
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "ExaClient":
        headers = {EXA_AUTH_HEADER: self.api_key}
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=headers,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        return self

    async def __aexit__(self, *args: Any) -> None:
        if self._client:
            await self._client.aclose()

    async def search(
        self,
        query: str,
        num_results: int = 10,
        mode: str = "auto",
        domains: list[str] | None = None,
        categories: list[str] | None = None,
        start_published_date: str | None = None,
        end_published_date: str | None = None,
        include_domains: list[str] | None = None,
        exclude_domains: list[str] | None = None,
    ) -> dict[str, Any]:
        """Call the Exa search endpoint."""
        if not self._client:
            raise RuntimeError("ExaClient must be used as an async context manager")

        payload: dict[str, Any] = {
            "query": query,
            "num_results": num_results,
            "mode": mode,
        }
        if domains:
            payload["domains"] = domains
        if categories:
            payload["categories"] = categories
        if start_published_date:
            payload["start_published_date"] = start_published_date
        if end_published_date:
            payload["end_published_date"] = end_published_date
        if include_domains:
            payload["include_domains"] = include_domains
        if exclude_domains:
            payload["exclude_domains"] = exclude_domains

        response = await self._client.post(SEARCH_ENDPOINT, json=payload)
        response.raise_for_status()
        return response.json()

    async def contents(
        self,
        ids: list[str],
        text: bool = True,
        highlights: bool = False,
        summaries: bool = False,
    ) -> dict[str, Any]:
        """Call the Exa contents endpoint."""
        if not self._client:
            raise RuntimeError("ExaClient must be used as an async context manager")

        payload: dict[str, Any] = {
            "ids": ids,
            "text": text,
            "highlights": highlights,
            "summaries": summaries,
        }

        response = await self._client.post(CONTENTS_ENDPOINT, json=payload)
        response.raise_for_status()
        return response.json()

    async def find_similar(
        self,
        url: str | None = None,
        result_id: str | None = None,
        num_results: int = 10,
    ) -> dict[str, Any]:
        """Call the Exa find-similar endpoint."""
        if not self._client:
            raise RuntimeError("ExaClient must be used as an async context manager")

        if not url and not result_id:
            raise ValueError("Either 'url' or 'result_id' must be provided")

        payload: dict[str, Any] = {"num_results": num_results}
        if url:
            payload["url"] = url
        if result_id:
            payload["id"] = result_id

        response = await self._client.post(FIND_SIMILAR_ENDPOINT, json=payload)
        response.raise_for_status()
        return response.json()