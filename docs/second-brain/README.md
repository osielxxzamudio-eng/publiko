# Segundo Cerebro — Base de Conocimiento

Este directorio alberga un "segundo cerebro" personal basado en el método **PARA** (Projects, Areas, Resources, Archives) de Tiago Forte, adaptado al repositorio `publiko`.

## Estructura

```
docs/second-brain/
├── README.md            # Esta guía
├── projects/            # Proyectos activos con objetivo definido y fecha de fin
├── areas/               # Áreas de responsabilidad de largo plazo (sin fecha de fin)
├── resources/           # Temas de interés y referencia sin obligación activa
└── archives/            # Elementos de las tres categorías anteriores ya completados o inactivos
```

## Método PARA

| Carpeta | Propósito | Ejemplos |
|---------|-----------|----------|
| `projects/` | Iniciativas con resultado concreto y fecha límite | Crear sitio web, escribir artículo, configurar CI/CD |
| `areas/` | Responsabilidades que requieren mantenimiento continuo | Finanzas, salud, documentación del equipo, infraestructura |
| `resources/` | Información de referencia sobre temas de interés | Tutoriales de Git, notas de conferencia, enlaces útiles |
| `archives/` | Proyectos, áreas o recursos ya no activos | Proyecto terminado v1, área descontinuada |

## Cómo usar

1. Crea una nota en Markdown dentro de la carpeta que corresponda.
2. Usa nombres descriptivos en inglés para los archivos (ej. `2026-10-27-nombre-del-proyecto.md`).
3. Cuando un proyecto finalice o un área deje de activarse, mueve la nota a `archives/`.
4. Revisa semanalmente `projects/` y `areas/` para mantener el sistema actualizado.

## Origen

Este segundo cerebro se construye localmente en el repositorio `publiko`. Dado que no se dispone de un toolkit de GitHub ni de búsqueda web vía Composio en este entorno, el contenido se alimenta de forma manual y mediante clonación directa de repositorios con `git` cuando se dispone de la URL.

---
*Mantener este archivo actualizado a medida que el proyecto evoluciona.*