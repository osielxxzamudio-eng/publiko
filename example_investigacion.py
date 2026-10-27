"""Example usage of the Investigacion skill."""

import asyncio
import os

from skills.investigacion import InvestigacionSkill


async def main() -> None:
    api_key = os.getenv("EXA_API_KEY")
    if not api_key:
        print("WARNING: EXA_API_KEY not set. Using placeholder.")
        api_key = "demo-key"

    skill = InvestigacionSkill(api_key=api_key)

    print("=== Investigación: IA en educación ===")
    try:
        response = await skill.research(
            topic="inteligencia artificial en educación",
            num_results=3,
        )
        print(f"Tema: {response.topic}")
        print(f"Resultados: {response.total_results}")
        for r in response.results:
            print(f"  - {r.title} | {r.source_type} | {r.url}")
    except Exception as exc:  # noqa: BLE001
        print(f"Error en investigación: {exc}")

    print("\n=== Metodología: energía renovable ===")
    try:
        method = await skill.methodology(
            topic="energía renovable",
            methodology_type="cuantitativa",
            num_results=3,
        )
        print(f"Tema: {method.topic}")
        print(f"Metodología: {method.methodology_type}")
        print(f"Resultados: {method.total_results}")
        for r in method.results:
            print(f"  - {r.title} | {r.url}")
    except Exception as exc:  # noqa: BLE001
        print(f"Error en metodología: {exc}")

    print("\n=== Revisión de literatura: teletrabajo ===")
    try:
        review = await skill.literature_review(
            research_question="¿cómo afecta el teletrabajo a la productividad?",
            key_concepts=["teletrabajo", "productividad", "trabajo remoto"],
            num_results=3,
        )
        print(f"Pregunta: {review.research_question}")
        print(f"Conceptos: {review.key_concepts}")
        print(f"Resultados: {review.total_results}")
        for r in review.results:
            print(f"  - {r.title} | {r.url}")
    except Exception as exc:  # noqa: BLE001
        print(f"Error en revisión de literatura: {exc}")


if __name__ == "__main__":
    asyncio.run(main())