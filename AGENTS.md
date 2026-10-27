# AGENTS.md

Este archivo proporciona instrucciones a los agentes de IA que trabajan en el repositorio `publiko`.

## Propósito del proyecto

[Describir aquí el propósito del proyecto `publiko`.]

## Estructura del repositorio

```
publiko/
├── README.md          # Documentación general del proyecto
├── AGENTS.md          # Instrucciones para agentes de IA (este archivo)
└── docs/
    └── second-brain/  # Base de conocimiento personal (segundo cerebro, método PARA)
        ├── README.md
        ├── proyectos/
        ├── áreas/
        ├── recursos/
        └── archivos/
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
2. Implementar los cambios.
3. Commit: `git add . && git commit -m "feat: descripción"`
4. Push: `git push origin feature/nombre`
5. Abrir un Pull Request hacia `main`.

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

## Verificación

- Antes de marcar una tarea como completada, ejecutar cualquier prueba o build disponible para confirmar que los cambios funcionan.
- No asumir que algo funciona sin verificar por ejecución.

## Notas

- El repositorio está en fase inicial de configuración. Las carpetas y dependencias aún no están definidas.
- Cualquier cambio estructural (nuevas carpetas, dependencias, scripts de build) debe documentarse en este archivo y en el `README.md`.

---

*Mantener este archivo actualizado a medida que el proyecto evoluciona.*