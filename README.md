# publiko

`publiko` es un **framework modular de skills** (módulos funcionales independientes) para agentes de IA. Cada skill vive bajo `skills/<nombre>/` siguiendo un patrón estandarizado de 6 archivos y puede verificarse y crearse nuevas mediante las propias herramientas del repositorio.

## Estado

✅ Estable — 4 skills implementadas y verificadas.

## Comenzando

### Requisitos previos

- Python 3.10+
- Una API key de Exa Labs (para las skills de búsqueda e investigación): `export EXA_API_KEY="tu-api-key"`

### Instalación

```bash
git clone https://github.com/osielxxzamudio-eng/publiko.git
cd publiko
pip install -r requirements.txt
```

### Uso

```bash
# Verificar que todas las skills están correctas
python verify_skills.py

# Ejecutar las pruebas unitarias
python -m pytest tests/ -v

# Ver ejemplos de uso (web_search, investigacion, skill_create, skill_verification)
python example_usage.py
python example_investigacion.py
python example_skill_create.py
python example_skill_verification.py
```

## Skills disponibles

| Skill | Propósito | Operaciones principales |
|-------|-----------|----------------------|
| `web_search` | Búsqueda web vía API de Exa Labs | `search`, `contents`, `find_similar` |
| `investigacion` | Investigación académica vía Exa Labs | `research`, `methodology`, `literature_review` |
| `skill_create` | Scaffolder: crea/valida/lista skills | `scaffold`, `validate`, `list_skills`, `generate_file` |
| `skill_verification` | Verifica la integridad de todas las skills | `verify_all`, `verify_skill`, `repository_health` |

## Estructura del proyecto

```
publiko/
├── README.md                          # Documentación general del proyecto
├── AGENTS.md                          # Instrucciones para agentes de IA
├── verify_skills.py                   # Script CLI de verificación de todas las skills
├── requirements.txt                   # Dependencias del proyecto
├── example_usage.py                   # Ejemplo de uso de web_search
├── example_investigacion.py           # Ejemplo de uso de investigacion
├── example_skill_create.py            # Ejemplo de uso de skill_create
├── example_skill_verification.py      # Ejemplo de uso de skill_verification
├── skills/                            # Directorio de skills
│   ├── web_search/
│   ├── investigacion/
│   ├── skill_create/
│   └── skill_verification/
├── tests/                             # Pruebas unitarias
└── docs/
    └── second-brain/                  # Base de conocimiento personal (método PARA)
        ├── README.md
        ├── proyectos/
        ├── áreas/
        ├── recursos/
        └── archivos/
```

## Patrón de una skill

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

Consulte `AGENTS.md` para las reglas detalladas de creación y verificación de skills.

## Contribuir

1. Haz un fork del repositorio
2. Crea una rama (`git checkout -b feature/nombre`)
3. Implementa siguiendo el patrón de skill
4. Verifica: `python verify_skills.py` y `python -m pytest tests/ -v`
5. Commit tus cambios (`git commit -m 'feat: descripción'`)
6. Push a la rama (`git push origin feature/nombre`)
7. Abre un Pull Request hacia `main`

## Licencia

[Especificar licencia]

---

## Cómo hacer buenos archivos README

Un buen README es la carta de presentación de tu proyecto. Sigue estas recomendaciones para escribirlo bien:

### Estructura recomendada

1. **Título y descripción breve** — Nombre del proyecto y una frase de qué trata.
2. **Estado** — Indicador de madurez (ej. 🚧 en desarrollo, ✅ estable).
3. **Comenzando / Requisitos previos** — Qué se necesita antes de usar el proyecto.
4. **Instalación** — Comandos para instalar dependencias y poner el proyecto en marcha.
5. **Uso** — Ejemplos claros de cómo usar el proyecto (bloques de código).
6. **Estructura del proyecto** — Árbol de carpetas con el propósito de cada una.
7. **Contribuir** — Pasos para hacer fork, rama, commit y pull request.
8. **Licencia** — Licencia bajo la cual se distribuye el proyecto.

### Buenas prácticas

- Usa encabezados claros y jerárquicos (`#`, `##`, `###`).
- Incluye bloques de código con el lenguaje especificado (ej. ```bash).
- Usa listas y tablas para organizar información.
- Mantén el lenguaje claro y conciso; evita jerga innecesaria.
- Actualiza el README cada vez que cambie la instalación o el uso del proyecto.
- Agrega un emoji de estado al inicio para dar contexto rápido.

### Ejemplo de bloque de instalación

```bash
git clone https://github.com/usuario/proyecto.git
cd proyecto
# instrucciones de instalación
```

---

*Desarrollado con ❤️ por [osielxxzamudio-eng](https://github.com/osielxxzamudio-eng)*