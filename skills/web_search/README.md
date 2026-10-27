# Web Search Skill (Exa Labs)

Skill para buscar en la web usando la API de **Exa Labs** (antes Metaphor).

## Endpoints soportados

| Operación | Endpoint Exa | Descripción |
|-----------|--------------|-------------|
| `search` | `POST /search` | Búsqueda general con modos neural/keyword/auto y filtros |
| `contents` | `POST /contents` | Extraer texto, highlights y resúmenes de resultados |
| `find_similar` | `POST /find-similar` | Encontrar páginas similares a una URL o ID |

## Instalación

```bash
pip install -r requirements.txt
```

## Configuración

Define tu API key de Exa Labs como variable de entorno:

```bash
export EXA_API_KEY="tu-api-key-aqui"
```

Opcionalmente puedes sobrescribir la URL base:

```bash
export EXA_API_BASE_URL="https://api.exa.ai"
```

## Uso

```python
import asyncio
from skills.web_search import WebSearchSkill


async def main() -> None:
    skill = WebSearchSkill()

    # Búsqueda general
    response = await skill.search(
        query="inteligencia artificial 2026",
        num_results=5,
        mode="neural",
    )
    for result in response.results:
        print(f"- {result.title}: {result.url}")

    # Extraer contenidos de resultados
    ids = [r.url for r in response.results[:3]]
    contents = await skill.contents(ids=ids, text=True, summaries=True)

    # Buscar páginas similares
    similar = await skill.find_similar(url="https://example.com", num_results=5)


asyncio.run(main())
```

## Requerimientos

- Python 3.10+
- `httpx`
- `pydantic`

## Licencia

[Especificar licencia]