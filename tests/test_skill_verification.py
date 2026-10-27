"""Unit tests for the Skill Verification skill."""

import sys
import tempfile
from pathlib import Path

from skills.skill_verification.skill import SkillVerificationSkill


def test_verify_all_empty_directory() -> None:
    """Verify all should return empty results when no skills exist."""
    with tempfile.TemporaryDirectory() as tmpdir:
        verifier = SkillVerificationSkill(skills_dir=tmpdir)
        result = verifier.verify_all()

        assert result.total_skills == 0
        assert result.valid_skills == 0
        assert result.invalid_skills == 0
        assert result.all_valid is False
        assert "No se encontró el directorio de skills" in result.summary or "No se encontraron skills" in result.summary


def test_verify_all_with_valid_skills() -> None:
    """Verify all should count valid skills correctly."""
    with tempfile.TemporaryDirectory() as tmpdir:
        skills_dir = Path(tmpdir) / "skills"
        skills_dir.mkdir()
        verifier = SkillVerificationSkill(skills_dir=str(skills_dir))

        # Crear una skill válida en skills/test_skill/
        skill_path = skills_dir / "test_skill"
        skill_path.mkdir()
        (skill_path / "__init__.py").write_text(
            '"""Test skill."""\nfrom .skill import TestSkillSkill\n\n__all__ = ["TestSkillSkill"]\n__version__ = "1.0.0"\n'
        )
        (skill_path / "config.py").write_text("import os\nAPI_KEY = os.getenv(\"API_KEY\", \"\")\n")
        (skill_path / "models.py").write_text("from pydantic import BaseModel\n")
        (skill_path / "client.py").write_text("import httpx\n")
        (skill_path / "skill.py").write_text(
            "class TestSkillSkill:\n    pass\n"
        )
        (skill_path / "README.md").write_text(
            "# Test Skill\n\n## Instalación\n\n## Uso\n\n"
        )

        sys.path.insert(0, tmpdir)
        result = verifier.verify_all()

        assert result.total_skills == 1
        assert result.valid_skills == 1
        assert result.invalid_skills == 0
        assert result.all_valid is True


def test_verify_skill_nonexistent() -> None:
    """Verify skill should return invalid for non-existent skill."""
    verifier = SkillVerificationSkill(skills_dir="/tmp/nonexistent")
    result = verifier.verify_skill("no_existe")

    assert result.valid is False
    assert result.skill_name == "no_existe"
    assert len(result.errors) > 0


def test_check_imports_valid() -> None:
    """Check imports should return True for existing skills."""
    verifier = SkillVerificationSkill(skills_dir="skills")
    # web_search e investigacion ya existen y son importables
    assert verifier.check_imports("web_search") is True
    assert verifier.check_imports("investigacion") is True


def test_check_imports_invalid() -> None:
    """Check imports should return False for non-existent skills."""
    verifier = SkillVerificationSkill(skills_dir="skills")
    assert verifier.check_imports("skill_no_existe") is False


def test_check_structure_valid() -> None:
    """Check structure should return True for complete skills."""
    verifier = SkillVerificationSkill(skills_dir="skills")
    assert verifier.check_structure("web_search") is True
    assert verifier.check_structure("investigacion") is True


def test_check_structure_invalid() -> None:
    """Check structure should return False for incomplete skills."""
    verifier = SkillVerificationSkill(skills_dir="skills")
    assert verifier.check_structure("skill_no_existe") is False


def test_check_readme_valid() -> None:
    """Check readme should return True for skills with proper README."""
    verifier = SkillVerificationSkill(skills_dir="skills")
    assert verifier.check_readme("web_search") is True
    assert verifier.check_readme("investigacion") is True


def test_repository_health() -> None:
    """Repository health should return a health report."""
    verifier = SkillVerificationSkill(skills_dir="skills")
    health = verifier.repository_health()

    assert isinstance(health.healthy, bool)
    assert health.total_skills >= 2  # web_search e investigacion
    assert health.valid_skills + health.invalid_skills == health.total_skills