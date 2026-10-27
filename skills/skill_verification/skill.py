"""Skill Verification — verifica que todas las skills del repositorio estén bien."""

import importlib
from pathlib import Path
from typing import Any

from .config import REQUIRED_FILES, REQUIRED_README_SECTIONS, SKILLS_DIR
from .models import (
    RepositoryHealthResponse,
    SkillCheckResult,
    VerifyAllResponse,
    VerifySkillResponse,
)


class SkillVerificationSkill:
    """Skill para verificar que todas las skills del repositorio estén correctas."""

    def __init__(self, skills_dir: str | None = None) -> None:
        self.skills_dir = Path(skills_dir or SKILLS_DIR)

    def verify_all(self) -> VerifyAllResponse:
        """Verificar todas las skills del repositorio."""
        results: list[SkillCheckResult] = []

        if not self.skills_dir.exists():
            return VerifyAllResponse(
                total_skills=0,
                valid_skills=0,
                invalid_skills=0,
                results=[],
                all_valid=False,
                summary=f"No se encontró el directorio de skills: {self.skills_dir}",
            )

        for entry in sorted(self.skills_dir.iterdir()):
            if not entry.is_dir():
                continue

            result = self._check_single_skill(entry.name, entry)
            results.append(result)

        valid_count = sum(1 for r in results if r.valid)
        invalid_count = len(results) - valid_count
        all_valid = invalid_count == 0 and len(results) > 0

        summary = self._build_summary(results, valid_count, invalid_count)

        return VerifyAllResponse(
            total_skills=len(results),
            valid_skills=valid_count,
            invalid_skills=invalid_count,
            results=results,
            all_valid=all_valid,
            summary=summary,
        )

    def verify_skill(self, skill_name: str) -> VerifySkillResponse:
        """Verificar una skill específica por nombre."""
        skill_path = self.skills_dir / skill_name

        if not skill_path.exists() or not skill_path.is_dir():
            return VerifySkillResponse(
                skill_name=skill_name,
                valid=False,
                missing_files=list(REQUIRED_FILES),
                errors=[f"La skill '{skill_name}' no existe en {skill_path}"],
                warnings=[],
                import_ok=False,
                structure_ok=False,
                readme_ok=False,
            )

        result = self._check_single_skill(skill_name, skill_path)

        return VerifySkillResponse(
            skill_name=result.skill_name,
            valid=result.valid,
            missing_files=result.missing_files,
            errors=result.errors,
            warnings=result.warnings,
            import_ok=result.import_ok,
            structure_ok=result.structure_ok,
            readme_ok=result.readme_ok,
        )

    def check_imports(self, skill_name: str) -> bool:
        """Verificar que el import de una skill funcione correctamente."""
        try:
            module_name = f"skills.{skill_name}"
            importlib.import_module(module_name)
            return True
        except Exception:
            return False

    def check_structure(self, skill_name: str) -> bool:
        """Verificar que una skill tenga todos los archivos requeridos."""
        skill_path = self.skills_dir / skill_name

        if not skill_path.exists() or not skill_path.is_dir():
            return False

        for required_file in REQUIRED_FILES:
            if not (skill_path / required_file).exists():
                return False

        return True

    def check_readme(self, skill_name: str) -> bool:
        """Verificar que el README de una skill tenga las secciones requeridas."""
        readme_path = self.skills_dir / skill_name / "README.md"

        if not readme_path.exists():
            return False

        content = readme_path.read_text(encoding="utf-8")

        for section in REQUIRED_README_SECTIONS:
            if section not in content:
                return False

        return True

    def repository_health(self) -> RepositoryHealthResponse:
        """Obtener el estado de salud del repositorio."""
        verification = self.verify_all()

        issues: list[str] = []
        recommendations: list[str] = []

        for result in verification.results:
            if not result.valid:
                issues.append(f"Skill '{result.skill_name}' no es válida")
                if result.missing_files:
                    issues.append(
                        f"  - Archivos faltantes: {', '.join(result.missing_files)}"
                    )
                if result.errors:
                    for error in result.errors:
                        issues.append(f"  - Error: {error}")
            if result.warnings:
                for warning in result.warnings:
                    recommendations.append(
                        f"Skill '{result.skill_name}': {warning}"
                    )

        if verification.invalid_skills > 0:
            recommendations.append(
                f"Revisar y corregir las {verification.invalid_skills} skill(s) inválida(s)"
            )

        if verification.total_skills == 0:
            issues.append("No se encontraron skills en el repositorio")
            recommendations.append(
                "Crear al menos una skill usando la skill 'skill_create'"
            )

        healthy = verification.all_valid and verification.total_skills > 0

        return RepositoryHealthResponse(
            healthy=healthy,
            total_skills=verification.total_skills,
            valid_skills=verification.valid_skills,
            invalid_skills=verification.invalid_skills,
            issues=issues,
            recommendations=recommendations,
        )

    def _check_single_skill(
        self, skill_name: str, skill_path: Path
    ) -> SkillCheckResult:
        missing_files: list[str] = []
        errors: list[str] = []
        warnings: list[str] = []

        structure_ok = True
        for required_file in REQUIRED_FILES:
            if not (skill_path / required_file).exists():
                missing_files.append(required_file)
                structure_ok = False

        init_file = skill_path / "__init__.py"
        if init_file.exists():
            init_content = init_file.read_text(encoding="utf-8")
            expected_class = (
                "".join(word.capitalize() for word in skill_name.split("_")) + "Skill"
            )
            expected_import = f"from .skill import {expected_class}"
            if expected_import not in init_content:
                warnings.append(
                    f"__init__.py no exporta la clase esperada '{expected_class}'"
                )
        else:
            missing_files.append("__init__.py")

        skill_file = skill_path / "skill.py"
        if skill_file.exists():
            skill_content = skill_file.read_text(encoding="utf-8")
            if "class " not in skill_content:
                errors.append("skill.py no contiene ninguna clase definida")
        else:
            missing_files.append("skill.py")
            errors.append("skill.py no se encuentra")

        readme_ok = self.check_readme(skill_name)
        import_ok = self.check_imports(skill_name)

        valid = (
            len(missing_files) == 0
            and len(errors) == 0
            and structure_ok
            and import_ok
            and readme_ok
        )

        return SkillCheckResult(
            skill_name=skill_name,
            skill_path=str(skill_path),
            valid=valid,
            missing_files=missing_files,
            errors=errors,
            warnings=warnings,
            import_ok=import_ok,
            structure_ok=structure_ok,
            readme_ok=readme_ok,
        )

    def _build_summary(
        self, results: list[SkillCheckResult], valid_count: int, invalid_count: int
    ) -> str:
        if not results:
            return "No se encontraron skills para verificar."

        if invalid_count == 0:
            return (
                f"Todas las {valid_count} skill(es) están válidas. "
                "El repositorio está en buen estado."
            )

        return (
            f"{valid_count} de {len(results)} skill(es) válida(s), "
            f"{invalid_count} inválida(s). "
            "Revisar los errores para corregir las skills problemáticas."
        )