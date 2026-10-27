"""Unit tests for the Web Search skill."""

import json
import pytest
from httpx import Request, Response

from skills.web_search.client import ExaClient
from skills.web_search.models import SearchRequest
from skills.web_search.skill import WebSearchSkill


def make_handler(payload: dict):
    """Return an async handler for httpx.MockTransport."""

    async def handler(request: Request) -> Response:
        return Response(200, json=payload)

    return handler


@pytest.mark.asyncio
async def test_search_returns_structured_results() -> None:
    fake_payload = {
        "results": [
            {
                "title": "Exa AI",
                "url": "https://exa.ai",
                "score": 0.95,
                "publishedDate": "2026-01-01",
                "author": "Exa Labs",
                "image": "https://exa.ai/logo.png",
                "snippet": "Web search API",
            }
        ]
    }

    transport = __import__("httpx").MockTransport(make_handler(fake_payload))

    async with ExaClient(api_key="test-key", base_url="https://api.exa.ai") as client:
        client._client._transport = transport  # type: ignore[attr-defined]
        data = await client.search(query="test query", num_results=5, mode="auto")

    assert data["results"][0]["title"] == "Exa AI"
    assert data["results"][0]["url"] == "https://exa.ai"


@pytest.mark.asyncio
async def test_skill_search_maps_to_response_model() -> None:
    """Skill.search maps Exa API response into SearchResponse model."""
    from unittest.mock import AsyncMock, patch

    fake_payload = {
        "results": [
            {
                "title": "Result One",
                "url": "https://example.com/one",
                "score": 0.8,
            }
        ]
    }

    mock_client = AsyncMock(spec=ExaClient)
    mock_client.search = AsyncMock(return_value=fake_payload)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    skill = WebSearchSkill(api_key="test-key")

    with patch("skills.web_search.skill.ExaClient", return_value=mock_client):
        response = await skill.search(query="hello world", num_results=1)

    assert response.query == "hello world"
    assert response.total_results == 1
    assert response.results[0].title == "Result One"
    assert response.results[0].url == "https://example.com/one"
    assert response.results[0].score == 0.8


def test_search_request_defaults() -> None:
    req = SearchRequest(query="q")
    assert req.num_results == 10
    assert req.mode == "auto"
    assert req.domains is None


@pytest.mark.asyncio
async def test_find_similar_requires_seed() -> None:
    skill = WebSearchSkill(api_key="test-key")
    with pytest.raises(ValueError, match="Either 'url' or 'result_id'"):
        await skill.find_similar(url=None, result_id=None)


@pytest.mark.asyncio
async def test_contents_endpoint() -> None:
    fake_payload = {"results": [{"id": "1", "text": "contido de ejemplo"}]}
    transport = __import__("httpx").MockTransport(make_handler(fake_payload))

    async with ExaClient(api_key="test-key", base_url="https://api.exa.ai") as client:
        client._client._transport = transport  # type: ignore[attr-defined]
        data = await client.contents(ids=["1"], text=True)

    assert data["results"][0]["text"] == "contido de ejemplo"


@pytest.mark.asyncio
async def test_find_similar_endpoint() -> None:
    fake_payload = {
        "results": [
            {
                "title": "Similar One",
                "url": "https://similar.example.com",
                "score": 0.7,
            }
        ]
    }
    transport = __import__("httpx").MockTransport(make_handler(fake_payload))

    async with ExaClient(api_key="test-key", base_url="https://api.exa.ai") as client:
        client._client._transport = transport  # type: ignore[attr-defined]
        data = await client.find_similar(url="https://example.com", num_results=3)

    assert data["results"][0]["title"] == "Similar One"
    assert data["results"][0]["score"] == 0.7