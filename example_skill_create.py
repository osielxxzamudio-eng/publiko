"""Example usage of the Skill Create skill."""

import os
from pathlib import Path

from skills.skill_create import SkillCreateSkill


def main() -> None:
    skills_dir = os.getenv("SKILLS_DIR", "skills")
    creator = SkillCreateSkill(skills_dir=skills_dir)

    print("=== Skills existentes ===")
    skills = creator.list_skills()
    print(f"Total: {skills.total}")
    for s in skills.skills:
        status = "✓" if s["valid"] else "✗"
        print(f"  {status} {s['name']} ({'válida' if s['valid'] else 'inválida'})")
        if s["missing_files"]:
            print(f"      Archivos faltantes: {s['missing_files']}")

    print("\n=== Scaffold de nueva skill ===")
    result = creator.scaffold(
        skill_name="example_new_skill",
        description="Una skill de ejemplo generada por Skill Create",
        version="1.0.0",
        author="Legion",
    )
    print(result.message)
    for f in result.files_created:
        print(f"  Creado: {f}")

    print("\n=== Validar la nueva skill ===")
    validation = creator.validate(f"{skills_dir}/example_new_skill")
    print(f"Válida: {validation.valid}")
    if validation.warnings:
        print(f"Advertencias: {validation.warnings}")

    print("\n=== Generar archivo individual ===")
    gen = creator.generate_file(
        skill_name="example_new_skill",
        file_type="config",
        description="Configuración de ejemplo",
    )
    print(f"Archivo: {gen.target_path}")
    print(f"Tipo: {gen.file_type}")
    print("Contenido generado correctamente.")


if __name__ == "__main__":
    main()