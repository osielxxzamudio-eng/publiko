# Investigacion Skill (Exa Labs)

Skill para buscar información de **investigación académica y científica** usando la API de **Exa Labs**.

## Operaciones

| Operación | Descripción |
|-----------|-------------|
| `research` | Búsqueda general de investigación sobre un tema académico |
| `methodology` | Buscar metodologías de investigación (cualitativa, cuantitativa, mixta, etc.) |
| `literature_review` | Recursos para revisión de literatura y revisiones sistemáticas |
| `contents` | Extraer texto completo y resúmenes de papers/artículos |
| `find_similar` | Encontrar papers similares a una URL o ID dado |

## Instalación

```bash
pip install -r requirements.txt
```

## Configuración

```bash
export EXA_API_KEY="tu-api-key-de-exa-labs"
```

## Uso

```python
import asyncio
from skills.investigacion import InvestigacionSkill


async def main() -> None:
    skill = InvestigacionSkill()

    # Buscar investigación sobre un tema
    response = await skill.research(
        topic="machine learning in healthcare",
        num_results=5,
    )
    for r in response.results:
        print(f"- {r.title} ({r.source_type}): {r.url}")

    # Buscar metodologías
    method = await skill.methodology(
        topic="climate change",
        methodology_type="mixed methods",
        num_results=5,
    )

    # Revisión de literatura
    review = await skill.literature_review(
        research_question="¿Cómo afecta el teletrabajo a la productividad?",
        key_concepts=["teletrabajo", "productividad", "trabajo remoto"],
        num_results=10,
    )


asyncio.run(main())
```

## Dominios académicos por defecto

La skill busca por defecto en dominios como: arxiv.org, researchgate.net, semanticscholar.org, ieee.org, acm.org, springer.com, sciencedirect.com, jstor.org, entre otros.

## Requerimientos

- Python 3.10+
- `httpx`
- `pydantic`

## Licencia

[Especificar licencia]