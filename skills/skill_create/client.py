"""HTTP client para la skill Skill Create.

Esta skill no llama a una API externa, pero incluye un cliente
placeholder para mantener la estructura consistente del repositorio.
"""

from typing import Any

import httpx

from .config import API_AUTH_HEADER, API_BASE_URL, API_KEY, REQUEST_TIMEOUT_SECONDS


class SkillCreateClient:
    """Cliente HTTP para operaciones de scaffrado de skills."""

    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:
        self.api_key = api_key or API_KEY
        self.base_url = base_url or API_BASE_URL
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "SkillCreateClient":
        headers = {API_AUTH_HEADER: self.api_key} if self.api_key else {}
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=headers,
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        return self

    async def __aexit__(self, *args: Any) -> None:
        if self._client:
            await self._client.aclose()

    async def ping(self) -> dict[str, Any]:
        """Comprueba que el cliente esté operativo."""
        return {"status": "ok", "service": "skill_create"}