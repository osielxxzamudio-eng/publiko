"""Example usage of the Web Search skill."""

import asyncio
import os

from skills.web_search import WebSearchSkill


async def main() -> None:
    api_key = os.getenv("EXA_API_KEY")
    if not api_key:
        print("WARNING: EXA_API_KEY not set. Using placeholder.")
        api_key = "demo-key"

    skill = WebSearchSkill(api_key=api_key)

    print("=== Búsqueda web ===")
    try:
        response = await skill.search(
            query="¿qué es la inteligencia artificial?",
            num_results=3,
            mode="auto",
        )
        print(f"Consulta: {response.query}")
        print(f"Resultados: {response.total_results}")
        for r in response.results:
            print(f"  - {r.title} | {r.url} | score={r.score}")
    except Exception as exc:  # noqa: BLE001
        print(f"Error en búsqueda: {exc}")

    print("\n=== Páginas similares ===")
    try:
        similar = await skill.find_similar(
            url="https://www.wikipedia.org",
            num_results=3,
        )
        print(f"Similares: {similar.total_results}")
        for r in similar.results:
            print(f"  - {r.title} | {r.url}")
    except Exception as exc:  # noqa: BLE001
        print(f"Error en find_similar: {exc}")


if __name__ == "__main__":
    asyncio.run(main())