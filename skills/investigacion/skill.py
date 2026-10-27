"""Investigacion skill — high-level interface for academic research via Exa Labs."""

from typing import Any

from .client import ExaClient
from .config import (
    ACADEMIC_DOMAINS,
    DEFAULT_NUM_RESULTS,
    DEFAULT_SEARCH_MODE,
    RESEARCH_CATEGORIES,
)
from .models import (
    LiteratureReviewRequest,
    LiteratureReviewResponse,
    MethodologyRequest,
    MethodologyResponse,
    ResearchRequest,
    ResearchResponse,
    ResearchResult,
)


class InvestigacionSkill:
    """Skill para buscar información de investigación académica usando Exa Labs.

    Proporciona operaciones:
        - research: búsqueda general de investigación sobre un tema
        - methodology: buscar metodologías de investigación específicas
        - literature_review: búsqueda para revisión de literatura
        - contents: extraer contenido completo de resultados
        - find_similar: encontrar papers similares a una seed
    """

    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:
        self.api_key = api_key
        self.base_url = base_url

    async def research(
        self,
        topic: str,
        num_results: int = DEFAULT_NUM_RESULTS,
        domains: list[str] | None = None,
        categories: list[str] | None = None,
        include_domains: list[str] | None = None,
        exclude_domains: list[str] | None = None,
        start_published_date: str | None = None,
        end_published_date: str | None = None,
    ) -> ResearchResponse:
        """Buscar información de investigación sobre un tema académico."""
        search_domains = domains or ACADEMIC_DOMAINS
        search_categories = categories or RESEARCH_CATEGORIES

        request = ResearchRequest(
            topic=topic,
            num_results=num_results,
            domains=search_domains,
            categories=search_categories,
            include_domains=include_domains,
            exclude_domains=exclude_domains,
            start_published_date=start_published_date,
            end_published_date=end_published_date,
        )

        async with ExaClient(api_key=self.api_key, base_url=self.base_url) as client:
            data = await client.search(
                query=request.topic,
                num_results=request.num_results,
                mode=DEFAULT_SEARCH_MODE,
                domains=request.domains,
                categories=request.categories,
                include_domains=request.include_domains,
                exclude_domains=request.exclude_domains,
                start_published_date=request.start_published_date,
                end_published_date=request.end_published_date,
            )

        results = [
            ResearchResult(
                title=item.get("title", ""),
                url=item.get("url", ""),
                score=item.get("score"),
                published_date=item.get("publishedDate"),
                author=item.get("author"),
                snippet=item.get("snippet"),
                source_type=self._infer_source_type(item.get("url", "")),
            )
            for item in data.get("results", [])
        ]

        return ResearchResponse(
            topic=request.topic,
            results=results,
            total_results=len(results),
            raw=data,
        )

    async def methodology(
        self,
        topic: str,
        methodology_type: str | None = None,
        num_results: int = DEFAULT_NUM_RESULTS,
    ) -> MethodologyResponse:
        """Buscar metodologías de investigación aplicables a un tema."""
        query = f"{topic} research methodology"
        if methodology_type:
            query = f"{topic} {methodology_type} methodology"

        request = MethodologyRequest(
            topic=topic,
            methodology_type=methodology_type,
            num_results=num_results,
        )

        async with ExaClient(api_key=self.api_key, base_url=self.base_url) as client:
            data = await client.search(
                query=query,
                num_results=request.num_results,
                mode=DEFAULT_SEARCH_MODE,
                domains=ACADEMIC_DOMAINS,
                categories=RESEARCH_CATEGORIES,
            )

        results = [
            ResearchResult(
                title=item.get("title", ""),
                url=item.get("url", ""),
                score=item.get("score"),
                published_date=item.get("publishedDate"),
                author=item.get("author"),
                snippet=item.get("snippet"),
                source_type=self._infer_source_type(item.get("url", "")),
            )
            for item in data.get("results", [])
        ]

        return MethodologyResponse(
            topic=request.topic,
            methodology_type=request.methodology_type,
            results=results,
            total_results=len(results),
            raw=data,
        )

    async def literature_review(
        self,
        research_question: str,
        key_concepts: list[str] | None = None,
        num_results: int = DEFAULT_NUM_RESULTS,
    ) -> LiteratureReviewResponse:
        """Buscar recursos para una revisión de literatura."""
        concepts_part = " ".join(key_concepts) if key_concepts else ""
        query = f"{research_question} {concepts_part} literature review systematic review"

        request = LiteratureReviewRequest(
            research_question=research_question,
            key_concepts=key_concepts,
            num_results=num_results,
        )

        async with ExaClient(api_key=self.api_key, base_url=self.base_url) as client:
            data = await client.search(
                query=query,
                num_results=request.num_results,
                mode=DEFAULT_SEARCH_MODE,
                domains=ACADEMIC_DOMAINS,
                categories=RESEARCH_CATEGORIES,
            )

        results = [
            ResearchResult(
                title=item.get("title", ""),
                url=item.get("url", ""),
                score=item.get("score"),
                published_date=item.get("publishedDate"),
                author=item.get("author"),
                snippet=item.get("snippet"),
                source_type=self._infer_source_type(item.get("url", "")),
            )
            for item in data.get("results", [])
        ]

        return LiteratureReviewResponse(
            research_question=request.research_question,
            key_concepts=request.key_concepts,
            results=results,
            total_results=len(results),
            raw=data,
        )

    async def contents(
        self,
        ids: list[str],
        text: bool = True,
        highlights: bool = False,
        summaries: bool = True,
    ) -> dict[str, Any]:
        """Extraer contenido completo (texto, resúmenes) de papers/artículos."""
        async with ExaClient(api_key=self.api_key, base_url=self.base_url) as client:
            data = await client.contents(
                ids=ids,
                text=text,
                highlights=highlights,
                summaries=summaries,
            )
        return data

    async def find_similar(
        self,
        url: str | None = None,
        result_id: str | None = None,
        num_results: int = DEFAULT_NUM_RESULTS,
    ) -> dict[str, Any]:
        """Encontrar papers/artículos similares a una URL o ID dado."""
        async with ExaClient(api_key=self.api_key, base_url=self.base_url) as client:
            data = await client.find_similar(
                url=url,
                result_id=result_id,
                num_results=num_results,
            )
        return data

    @staticmethod
    def _infer_source_type(url: str) -> str:
        """Inferir el tipo de fuente a partir de la URL."""
        url_lower = url.lower()
        if "arxiv.org" in url_lower:
            return "preprint"
        if "semanticscholar.org" in url_lower:
            return "paper"
        if "researchgate.net" in url_lower:
            return "paper"
        if "ieee.org" in url_lower or "acm.org" in url_lower:
            return "conference paper"
        if "springer.com" in url_lower or "sciencedirect.com" in url_lower:
            return "journal article"
        if "edu" in url_lower:
            return "academic resource"
        return "article"