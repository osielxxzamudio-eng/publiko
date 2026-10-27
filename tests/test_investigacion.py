"""Unit tests for the Investigacion skill."""

from unittest.mock import AsyncMock, patch

import pytest

from skills.investigacion.client import ExaClient
from skills.investigacion.models import ResearchRequest
from skills.investigacion.skill import InvestigacionSkill


def make_fake_payload(results: list[dict]) -> dict:
    return {"results": results}


@pytest.mark.asyncio
async def test_research_returns_structured_results() -> None:
    fake_payload = make_fake_payload([
        {
            "title": "AI in Healthcare",
            "url": "https://arxiv.org/abs/1234",
            "score": 0.92,
            "publishedDate": "2026-01-15",
            "author": "J. Doe",
            "snippet": "A study on AI in healthcare",
        }
    ])

    mock_client = AsyncMock(spec=ExaClient)
    mock_client.search = AsyncMock(return_value=fake_payload)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    skill = InvestigacionSkill(api_key="test-key")

    with patch("skills.investigacion.skill.ExaClient", return_value=mock_client):
        response = await skill.research(topic="AI healthcare", num_results=5)

    assert response.topic == "AI healthcare"
    assert response.total_results == 1
    assert response.results[0].title == "AI in Healthcare"
    assert response.results[0].url == "https://arxiv.org/abs/1234"
    assert response.results[0].score == 0.92
    assert response.results[0].source_type == "preprint"


@pytest.mark.asyncio
async def test_methodology_search() -> None:
    fake_payload = make_fake_payload([
        {
            "title": "Mixed Methods in Climate Research",
            "url": "https://researchgate.net/publication/123",
            "score": 0.85,
        }
    ])

    mock_client = AsyncMock(spec=ExaClient)
    mock_client.search = AsyncMock(return_value=fake_payload)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    skill = InvestigacionSkill(api_key="test-key")

    with patch("skills.investigacion.skill.ExaClient", return_value=mock_client):
        response = await skill.methodology(
            topic="climate change",
            methodology_type="mixed methods",
            num_results=5,
        )

    assert response.topic == "climate change"
    assert response.methodology_type == "mixed methods"
    assert response.total_results == 1
    assert response.results[0].title == "Mixed Methods in Climate Research"
    assert response.results[0].source_type == "paper"


@pytest.mark.asyncio
async def test_literature_review() -> None:
    fake_payload = make_fake_payload([
        {
            "title": "Remote Work Productivity Review",
            "url": "https://sciencedirect.com/article/123",
            "score": 0.88,
        }
    ])

    mock_client = AsyncMock(spec=ExaClient)
    mock_client.search = AsyncMock(return_value=fake_payload)
    mock_client.__aenter__ = AsyncMock(return_value=mock_client)
    mock_client.__aexit__ = AsyncMock(return_value=None)

    skill = InvestigacionSkill(api_key="test-key")

    with patch("skills.investigacion.skill.ExaClient", return_value=mock_client):
        response = await skill.literature_review(
            research_question="remote work productivity",
            key_concepts=["remote", "productivity"],
            num_results=5,
        )

    assert response.research_question == "remote work productivity"
    assert response.key_concepts == ["remote", "productivity"]
    assert response.total_results == 1
    assert response.results[0].title == "Remote Work Productivity Review"
    assert response.results[0].source_type == "journal article"


def test_research_request_defaults() -> None:
    req = ResearchRequest(topic="test topic")
    assert req.num_results == 10
    assert req.domains is None
    assert req.categories is None


def test_infer_source_type() -> None:
    skill = InvestigacionSkill(api_key="test-key")

    assert skill._infer_source_type("https://arxiv.org/abs/123") == "preprint"
    assert skill._infer_source_type("https://researchgate.net/pub/123") == "paper"
    assert skill._infer_source_type("https://ieee.org/document/123") == "conference paper"
    assert skill._infer_source_type("https://sciencedirect.com/article/123") == "journal article"
    assert skill._infer_source_type("https://mit.edu/paper") == "academic resource"
    assert skill._infer_source_type("https://example.com/blog") == "article"


@pytest.mark.asyncio
async def test_find_similar_requires_seed() -> None:
    skill = InvestigacionSkill(api_key="test-key")
    with pytest.raises(ValueError, match="Either 'url' or 'result_id'"):
        await skill.find_similar(url=None, result_id=None)