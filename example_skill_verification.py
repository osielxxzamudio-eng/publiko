"""Example usage of the Skill Verification skill."""

from skills.skill_verification import SkillVerificationSkill


def main() -> None:
    verifier = SkillVerificationSkill()

    print("=== Verificación de todas las skills ===")
    result = verifier.verify_all()
    print(result.summary)
    print(f"Válidas: {result.valid_skills}/{result.total_skills}")
    print()

    for r in result.results:
        status = "✓" if r.valid else "✗"
        print(f"{status} {r.skill_name}")
        if r.missing_files:
            print(f"   Faltan archivos: {r.missing_files}")
        if r.errors:
            print(f"   Errores: {r.errors}")
        if r.warnings:
            print(f"   Advertencias: {r.warnings}")
    print()

    print("=== Estado de salud del repositorio ===")
    health = verifier.repository_health()
    print(f"Saludable: {health.healthy}")
    print(f"Total skills: {health.total_skills}")
    print(f"Válidas: {health.valid_skills}")
    print(f"Inválidas: {health.invalid_skills}")
    if health.issues:
        print("Issues:")
        for issue in health.issues:
            print(f"  - {issue}")
    if health.recommendations:
        print("Recomendaciones:")
        for rec in health.recommendations:
            print(f"  - {rec}")
    print()

    print("=== Verificación individual ===")
    if result.results:
        first_skill = result.results[0].skill_name
        check = verifier.verify_skill(first_skill)
        print(f"Skill: {check.skill_name}")
        print(f"Válida: {check.valid}")
        print(f"Import OK: {check.import_ok}")
        print(f"Estructura OK: {check.structure_ok}")
        print(f"README OK: {check.readme_ok}")


if __name__ == "__main__":
    main()