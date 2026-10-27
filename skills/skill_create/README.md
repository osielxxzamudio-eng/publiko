# Skill Create Skill

Skill para crear y scafflear nuevas skills en el repositorio **publiko**.

## Operaciones

| Operación | Descripción |
|-----------|-------------|
| `scaffold` | Crear la estructura completa de una nueva skill |
| `validate` | Validar que una skill siga el patrón correcto |
| `list` | Listar todas las skills disponibles |
| `generate_file` | Generar el contenido de un archivo individual |

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```python
import asyncio
from skills.skill_create import SkillCreateSkill


def main() -> None:
    skill = SkillCreateSkill()

    # Scaffold de una nueva skill
    result = skill.scaffold(
        skill_name="mi_nueva_skill",
        description="Mi nueva skill para hacer X",
        version="1.0.0",
    )
    print(result.message)
    for f in result.files_created:
        print(f"  Creado: {f}")

    # Validar una skill existente
    validation = skill.validate("skills/mi_nueva_skill")
    print(f"Válida: {validation.valid}")
    if validation.errors:
        print(f"Errores: {validation.errors}")

    # Listar skills
    skills = skill.list_skills()
    print(f"Total skills: {skills.total}")


if __name__ == "__main__":
    main()
```

## Estructura de una skill

Cada skill sigue este patrón:

```
skills/<nombre_skill>/
├── __init__.py      # Exporta la clase principal
├── config.py        # Configuración y constantes
├── models.py        # Modelos Pydantic (request/response)
├── client.py        # Cliente HTTP async (httpx)
├── skill.py         # Lógica de alto nivel de la skill
└── README.md        # Documentación de la skill
```

## Requerimientos

- Python 3.10+
- `pydantic`

## Licencia

[Especificar licencia]