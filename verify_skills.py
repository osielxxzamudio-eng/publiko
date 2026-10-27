#!/usr/bin/env python3
"""Script CLI para verificar el estado de todas las skills del repositorio."""

import sys
from skills.skill_verification import SkillVerificationSkill


def main() -> None:
    verifier = SkillVerificationSkill()
    health = verifier.repository_health()

    print("=" * 60)
    print("  VERIFICACIÓN DE SKILLS — Repositorio Publiko")
    print("=" * 60)
    print()
    print(f"Repositorio saludable: {'SÍ ✓' if health.healthy else 'NO ✗'}")
    print(f"Total de skills: {health.total_skills}")
    print(f"Skills válidas: {health.valid_skills}")
    print(f"Skills inválidas: {health.invalid_skills}")
    print()

    print("-" * 60)
    print("  DETALLE POR SKILL")
    print("-" * 60)
    print()

    for i, r in enumerate(verifier.verify_all().results, 1):
        check = verifier.verify_skill(r.skill_name)
        status = "VÁLIDA ✓" if check.valid else "INVÁLIDA ✗"
        print(f"{i}. {r.skill_name}")
        print(f"   Ruta: {r.skill_path}")
        print(f"   Estado: {status}")
        print(f"   Import: {'OK' if check.import_ok else 'FALLA'}")
        print(f"   Estructura: {'OK' if check.structure_ok else 'FALLA'}")
        print(f"   README: {'OK' if check.readme_ok else 'FALLA'}")
        if check.missing_files:
            print(f"   Archivos faltantes: {', '.join(check.missing_files)}")
        if check.errors:
            print(f"   Errores: {'; '.join(check.errors)}")
        if check.warnings:
            print(f"   Advertencias: {'; '.join(check.warnings)}")
        print()

    if health.issues:
        print("-" * 60)
        print("  ISSUES ENCONTRADOS")
        print("-" * 60)
        for issue in health.issues:
            print(f"  • {issue}")
        print()

    if health.recommendations:
        print("-" * 60)
        print("  RECOMENDACIONES")
        print("-" * 60)
        for rec in health.recommendations:
            print(f"  • {rec}")
        print()

    print("=" * 60)
    if health.healthy:
        print("  TODAS LAS SKILLS ESTÁN CORRECTAS")
    else:
        print("  HAY SKILLS QUE REQUIEREN ATENCIÓN")
    print("=" * 60)

    sys.exit(0 if health.healthy else 1)


if __name__ == "__main__":
    main()