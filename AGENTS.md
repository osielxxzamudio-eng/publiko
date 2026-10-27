# AGENTS.md

Este archivo proporciona instrucciones a los agentes de IA que trabajan en el repositorio `publiko`.

## Propósito del proyecto

El repositorio `publiko` es un framework modular de **skills** (módulos funcionales independientes) que siguen un patrón estandarizado. Cada skill es un paquete Python autocontenido bajo `skills/<nombre>/` que implementa una funcionalidad específica (búsqueda web, investigación académica, generación de skills, verificación de skills, etc.).

El propósito es permitir que cualquier agente de IA pueda:
1. Crear nuevas skills siguiendo el patrón establecido.
2. Verificar que todas las skills del repositorio estén correctas.
3. Mantener consistencia estructural entre skills.

## Estructura del repositorio

```
publiko/
├── README.md                          # Documentación general del proyecto
├── AGENTS.md                          # Instrucciones para agentes de IA (este archivo)
├── verify_skills.py                   # Script CLI de verificación de todas las skills
├── requirements.txt                   # Dependencias del proyecto
├── example_usage.py                   # Ejemplo de uso de web_search
├── example_investigacion.py           # Ejemplo de uso de investigacion
├── example_skill_create.py            # Ejemplo de uso de skill_create
├── example_skill_verification.py      # Ejemplo de uso de skill_verification
├── skills/                            # Directorio de skills (cada subcarpeta es una skill)
│   ├── web_search/                    # Skill de búsqueda web (Exa Labs API)
│   ├── investigacion/                 # Skill de investigación académica (Exa Labs API)
│   ├── skill_create/                  # Skill para scafflear nuevas skills
│   └── skill_verification/            # Skill para verificar skills del repositorio
├── tests/                             # Pruebas unitarias
└── docs/
    └── second-brain/                  # Base de conocimiento personal (método PARA)
        ├── README.md
        ├── proyectos/
        ├── áreas/
        ├── recursos/
        └── archivos/
```

Cada skill contiene exactamente estos 6 archivos:
```
skills/<nombre_skill>/
├── __init__.py      # Exporta la clase principal: from .skill import <Nombre>Skill
├── config.py        # Constantes, variables de entorno, URLs, timeouts
├── models.py        # Modelos Pydantic (Request, Response, Result)
├── client.py        # Cliente HTTP async (httpx.AsyncClient)
├── skill.py         # Clase principal <Nombre>Skill con métodos de alto nivel
└── README.md        # Documentación: título (#), sección Instalación, sección Uso
```

## Entorno de ejecución — Cline Cloud

Los agentes de este repositorio operan dentro de **Cline Cloud**, una plataforma de agentes de IA (Cline, Inc.) que gestiona contenedores sandbox remotos. Todo el trabajo se ejecuta en la nube; no es necesario instalar nada localmente.

### Cómo funciona

- Cada interacción con el agente se guarda como un **"run"** asociado a una **session ID** (ej. `tsk-01M5Z546RSZNAXF8DA3DBGHZ3E`).
- El proveedor de modelo es `cline` (ej. `dots-studio/dots-3-note-preview:free`).
- El contenedor sandbox se monta como `/workspace` y es donde se clona el repositorio.
- GitHub authentication se inyecta transparentemente por el infraestructura; no se necesitan tokens ni `gh auth login`.

### La carpeta `.cline-home`

El directorio `.cline-home` es el **home local del agente dentro del sandbox**. Contiene metadatos de gestión interna:

| Ruta | Contenido |
|------|-----------|
| `.cline-home/data/sessions/tsk-<id>/tsk-<id>.json` | Datos de la session actual (modelo, rama de git, checkpoints, usage) |
| `.cline-home/data/sessions/tsk-<id>/tsk-<id>.messages.json` | Hilo completo de mensajes de la conversación |
| `.cline-home/data/db/*.db` | Bases de datos SQLite (sessions, tasks, teams, hubs, cron) |
| `.cline-home/rules/sandbox-resources.md` | Reglas de recursos del sandbox (CPU, memoria, disco) |
| `.cline-home/data/locks/` | Locks de instancias de hubs |
| `.cline-home/logs/hooks.jsonl` | Logs de hooks |

**No modifiques `.cline-home` a mano**; es de gestión interna del agente. Tampoco lo commites (está en `.gitignore`).

### Identificadores con esquema `cline://`

Las rutas como `cline://cache/tsk-<id>/...result.txt` son **identificadores internos del sistema Cline** que referencian archivos cacheados por el framework. No son archivos mágicos: son punteros a los artifacts generados durante una ejecución. No los uses como fuente de verdad; los datos reales siempre están en `/workspace`.

### Recursos del sandbox

- **CPU**: hasta 4 vCPU (no uses `nproc` para calcular paralelismo; el host tiene más núcleos pero tú no).
- **Memoria**: 6 GiB límite duro. El contenedor del agente y todos los procesos que inicia comparten este límite.
- **Disco**: 16 Gi para `/workspace` y el home. Escrituras fuera de `/workspace` (ej. `/tmp`) están limitadas a 4 Gi.

### Comunicación con el usuario

- Presentate siempre en español.
- Presentate siempre con el nombre **Legion** al iniciar una interacción.
- No asumas que algo funciona sin verificar por ejecución.

## Estructura mental para crear una skill (patrón obligatorio)

### Reglas del patrón:

1. **Nombre de la carpeta**: `snake_case` (ej. `web_search`, `investigacion`).
2. **Nombre de la clase**: `PascalCase` + sufijo `Skill` (ej. `WebSearchSkill`, `InvestigacionSkill`).
3. **`__init__.py`**: Debe exportar la clase: `from .skill import <Nombre>Skill` y definir `__all__ = ["<Nombre>Skill"]`.
4. **`config.py`**: Usar `os.getenv()` para variables de entorno (ej. `API_KEY`, `API_BASE_URL`). Incluir `API_AUTH_HEADER = "x-api-key"` y `REQUEST_TIMEOUT_SECONDS = 30`.
5. **`models.py`**: Usar Pydantic `BaseModel` con `Field()`. Clases: `<Nombre>Request`, `<Nombre>Result`, `<Nombre>Response`.
6. **`client.py`**: Clase con `async def __aenter__` y `async def __aexit__`. Usar `httpx.AsyncClient`.
7. **`skill.py`**: Clase `<Nombre>Skill` con métodos async que usen el cliente dentro de `async with`.
8. **`README.md`**: Debe contener `# <Título>`, `## Instalación`, `## Uso`.

### Criterios de validación (una skill es válida solo si TODO pasa):

1. Existen los 6 archivos requeridos.
2. `import skills.<nombre>` funciona sin errores.
3. `skill.py` contiene al menos una clase `class ...`.
4. `__init__.py` exporta `from .skill import <Nombre>Skill`.
5. `README.md` tiene `# `, `## Instalación`, `## Uso`.

## Skill Create (scaffledor de nuevas skills)

La skill `skill_create` permite generar automáticamente la estructura de una nueva skill.

### Operaciones:
- `scaffold(skill_name, description, version, author)` — Crea todos los 6 archivos.
- `validate(skill_path)` — Valida que una skill siga el patrón.
- `list_skills()` — Lista todas las skills con su estado.
- `generate_file(skill_name, file_type, description)` — Genera contenido de un archivo individual.

### Uso:
```python
from skills.skill_create import SkillCreateSkill

creator = SkillCreateSkill()
result = creator.scaffold(
    skill_name="mi_nueva_skill",
    description="Mi nueva skill para hacer X",
    version="1.0.0",
)
```

## Skill Verification (verificador de skills)

La skill `skill_verification` verifica que todas las skills del repositorio estén correctas.

### Operaciones:
- `verify_all()` — Verifica todas las skills y retorna resumen.
- `verify_skill(skill_name)` — Verifica una skill específica.
- `check_imports(skill_name)` — Verifica que el import funcione.
- `check_structure(skill_name)` — Verifica los 6 archivos requeridos.
- `check_readme(skill_name)` — Verifica secciones del README.
- `repository_health()` — Estado de salud general del repositorio.

### Script CLI:
```bash
python verify_skills.py
```

## Segundo Cerebro — Cómo se usa

El repositorio incluye una base de conocimiento personal bajo `docs/second-brain/` siguiendo el método **PARA** (Projects, Areas, Resources, Archives):

| Carpeta | Propósito |
|---------|-----------|
| `proyectos/` | Iniciativas con resultado concreto y fecha límite |
| `áreas/` | Responsabilidades que requieren mantenimiento continuo |
| `recursos/` | Información de referencia sobre temas de interés |
| `archivos/` | Proyectos, áreas o recursos ya no activos |

### Pasos para usar

1. Crea una nota en Markdown dentro de la carpeta que corresponda.
2. Usa nombres descriptivos en inglés para los archivos (ej. `2026-10-27-configurar-ci-cd.md`).
3. Cuando un proyecto finalice o un área deje de activarse, mueve la nota a `archivos/`.
4. Revisa semanalmente `proyectos/` y `áreas/` para mantener el sistema actualizado.

## Ramas de trabajo

- `main` — rama principal (estable, producción)
- `cline/a0qe8ypq` — rama de trabajo del agente Cline (backup de progreso)

Toda la implementación debe hacerse en ramas de feature y fusionarse mediante Pull Requests a `main`.

## Convenciones de código

- Usar nombres descriptivos en inglés para variables, funciones y archivos.
- Commits con mensajes claros siguiendo el formato: `tipo: descripción breve`
  - Ejemplos: `feat: ...`, `fix: ...`, `docs: ...`, `refactor: ...`
- No dejar código comentado ni `TODO`s sin resolver en commits finales.

## Flujo de trabajo recomendado

1. Crear una rama desde `main`: `git checkout -b feature/nombre`
2. Implementar los cambios siguiendo el patrón de skill.
3. Ejecutar tests: `python -m pytest tests/ -v`
4. Ejecutar verificación: `python verify_skills.py`
5. Commit: `git add . && git commit -m "feat: descripción"`
6. Push: `git push origin feature/nombre`
7. Abrir un Pull Request hacia `main`.

## Idioma

- Responder siempre en español.

## Sube cambios al repositorio

- Sube siempre los cambios al repositorio remoto tras cada commit.

## Reglas del agente

1. Responder siempre en español.
2. Usar nombres descriptivos en inglés para variables, funciones y archivos.
3. Commits con mensajes claros siguiendo el formato `tipo: descripción breve` (ej. `feat:`, `fix:`, `docs:`, `refactor:`).
4. No dejar código comentado ni `TODO`s sin resolver en commits finales.
5. Toda implementación debe hacerse en ramas de feature y fusionarse mediante Pull Requests a `main`.
6. Subir siempre los cambios al repositorio remoto tras cada commit.
7. Antes de marcar una tarea como completada, ejecutar pruebas o build para verificar que los cambios funcionan.
8. No asumir que algo funciona sin verificar por ejecución.
9. Cualquier cambio estructural debe documentarse en `AGENTS.md` y `README.md`.
10. Usar ramas de trabajo dedicadas (`feature/nombre`) y nunca commitear directamente a `main`.

11. Verificar dependencias antes de usarlas — Solo usar librerías y frameworks confirmados como compatibles con el código base actual.
12. Escribir código completo y funcional — No dejar omisiones, placeholders ni implementaciones a medias sin terminar.
13. Mantener commits atómicos — Cada commit debe contener cambios relacionados a una sola tarea o propósito claro.
14. Revisar el diff antes de pushear — Revisar `git diff` y `git status` antes de hacer commit y push para evitar archivos no deseados.
15. No commitear secrets ni credenciales — Nunca subir claves API, tokens, contraseñas o archivos `.env` con valores reales al repositorio.
16. Escribir mensajes de commit en español o inglés consistente — Mantener un idioma uniforme en todos los mensajes de commit del repositorio.
17. Limpiar archivos temporales antes de pushear — Eliminar archivos de compilación, logs, caches y directorios `node_modules`/`__pycache__` antes de hacer commit.
18. Documentar decisiones de arquitectura — Registrar en `AGENTS.md` o `README.md` cualquier decisión estructural importante que afecte al proyecto.
19. Probar en el entorno local antes de pushear — Ejecutar el programa, script o comando modificado localmente para confirmar que funciona como se espera.
20. Mantener las ramas actualizadas con `main` — Hacer `git pull` o rebase frecuente de `main` en la rama de trabajo para evitar conflictos de fusión.
21. Presentarse siempre en español al iniciar una interacción con el usuario.
22. Presentarse siempre con el nombre "Legion" al iniciar una interacción con el usuario.
23. **Al crear una nueva skill, seguir exactamente el patrón de 6 archivos** (`__init__.py`, `config.py`, `models.py`, `client.py`, `skill.py`, `README.md`).
24. **Después de crear o modificar skills, ejecutar `python verify_skills.py` y `python -m pytest tests/ -v`** antes de considerar la tarea completa.
25. **Usar la skill `skill_create` para scafflear nuevas skills** en lugar de crear archivos manualmente.

## Verificación

- Antes de marcar una tarea como completada, ejecutar cualquier prueba o build disponible para confirmar que los cambios funcionan.
- No asumir que algo funciona sin verificar por ejecución.
- Ejecutar `python -m pytest tests/ -v` — todos los tests deben pasar.
- Ejecutar `python verify_skills.py` — todas las skills deben ser válidas.

## Notas

- El repositorio cuenta con 4 skills implementadas y verificadas: `web_search`, `investigacion`, `skill_create`, `skill_verification`.
- Cualquier cambio estructural (nuevas carpetas, dependencias, scripts de build) debe documentarse en este archivo y en el `README.md`.
- No commitear secrets ni credenciales. Usar variables de entorno (`EXA_API_KEY`, `API_KEY`).

---

*Mantener este archivo actualizado a medida que el proyecto evoluciona.*