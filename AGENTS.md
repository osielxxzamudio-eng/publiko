# AGENTS.md

Este archivo proporciona instrucciones a los agentes de IA que trabajan en el repositorio `publiko`.

## Propósito del proyecto

[Describir aquí el propósito del proyecto `publiko`.]

## Estructura del repositorio

```
publiko/
├── README.md          # Documentación general del proyecto
├── AGENTS.md          # Instrucciones para agentes de IA (este archivo)
└── ...
```

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

## Verificación

- Antes de marcar una tarea como completada, ejecutar cualquier prueba o build disponible para confirmar que los cambios funcionan.
- No asumir que algo funciona sin verificar por ejecución.

## Notas

- El repositorio está en fase inicial de configuración. Las carpetas y dependencias aún no están definidas.
- Cualquier cambio estructural (nuevas carpetas, dependencias, scripts de build) debe documentarse en este archivo y en el `README.md`.

---

*Mantener este archivo actualizado a medida que el proyecto evoluciona.*