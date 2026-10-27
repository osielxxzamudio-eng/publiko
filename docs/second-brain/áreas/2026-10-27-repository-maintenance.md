# Repository Maintenance — Área de Responsabilidad

## Propósito

Esta área documenta la **responsabilidad continua de mantenimiento del repositorio `publiko`**, asistida por **Legion**, el agente de IA encargado de cuidar y desarrollar el framework modular de skills.

Legion es el encargado de:
1. Mantener actualizada la rama de trabajo `cline/a0qe8ypq` al día con `origin/main`.
2. Garantizar que todas las skills sigan el patrón de 6 archivos.
3. Ejecutar `python verify_skills.py` y `python -m pytest tests/ -v` tras cada cambio.
4. Mantener la documentación (`AGENTS.md`, `README.md`, notas del segundo cerebro) actualizada.
5. Resolver issues y Pull Requests de forma oportuna.
6. Asegurar que se suban los cambios al remoto tras cada commit.

## Métricas de salud

| Métrica | Status |
|--------|--------|
| Verificación de skills (`verify_skills.py`) | ✅ 4/4 válidas |
| Tests unitarios (`pytest`) | ✅ 30/30 pasan |
| Rama sincronizada con `main` | ✅ Sí |

## Revisiones periódicas

- Revisar semanalmente el estado del repositorio y la sincronía con `main`.
- Revisar semanalmente `docs/second-brain/proyectos/` y `áreas/` para mantener el sistema actualizado.