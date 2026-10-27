# Skill Verification Skill

Skill para verificar que todas las skills del repositorio **publiko** estén correctas y sigan el patrón establecido.

## Operaciones

| Operación | Descripción |
|-----------|-------------|
| `verify_all` | Verificar todas las skills del repositorio |
| `verify_skill` | Verificar una skill específica por nombre |
| `check_imports` | Verificar que los imports de una skill funcionen |
| `check_structure` | Verificar la estructura de archivos de una skill |
| `check_readme` | Verificar que el README tenga las secciones requeridas |
| `repository_health` | Obtener el estado de salud del repositorio |

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```python
from skills.skill_verification import SkillVerificationSkill


def main() -> None:
    verifier = SkillVerificationSkill()

    # Verificar todas las skills
    result = verifier.verify_all()
    print(result.summary)
    print(f"Válidas: {result.valid_skills}/{result.total_skills}")

    # Verificar una skill específica
    check = verifier.verify_skill("web_search")
    print(f"web_search válida: {check.valid}")

    # Estado de salud del repositorio
    health = verifier.repository_health()
    print(f"Repositorio saludable: {health.healthy}")
    if health.issues:
        print("Issues:")
        for issue in health.issues:
            print(f"  - {issue}")


if __name__ == "__main__":
    main()
```

## Verificaciones realizadas

Para cada skill se verifica:

1. **Estructura de archivos**: Existencia de `__init__.py`, `config.py`, `models.py`, `client.py`, `skill.py`, `README.md`
2. **Importación**: Que el módulo se pueda importar sin errores
3. **Clase en skill.py**: Que el archivo `skill.py` contenga al menos una clase definida
4. **Export en __init__.py**: Que exporte la clase correcta (ej. `from .skill import WebSearchSkill`)
5. **README**: Que tenga título (`# `), sección de Instalación y sección de Uso

## Requerimientos

- Python 3.10+

## Licencia

[Especificar licencia]