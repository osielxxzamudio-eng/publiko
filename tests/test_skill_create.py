"""Unit tests for the Skill Create skill."""

import os
import tempfile
from pathlib import Path

from skills.skill_create.skill import SkillCreateSkill


def test_scaffold_creates_skill_structure() -> None:
    """Scaffold should create all required files for a new skill."""
    with tempfile.TemporaryDirectory() as tmpdir:
        creator = SkillCreateSkill(skills_dir=tmpdir)
        result = creator.scaffold(
            skill_name="test_skill",
            description="A test skill",
            version="1.0.0",
        )

        assert result.skill_name == "test_skill"
        assert result.files_created
        assert "La skill 'test_skill' creada exitosamente" in result.message

        skill_path = Path(tmpdir) / "test_skill"
        for required in [
            "__init__.py",
            "config.py",
            "models.py",
            "client.py",
            "skill.py",
            "README.md",
        ]:
            assert (skill_path / required).exists(), f"Falta {required}"


def test_scaffold_duplicate_skill() -> None:
    """Scaffolding an existing skill should return a message, not overwrite."""
    with tempfile.TemporaryDirectory() as tmpdir:
        creator = SkillCreateSkill(skills_dir=tmpdir)
        creator.scaffold(skill_name="test_skill", description="First")
        result = creator.scaffold(skill_name="test_skill", description="Second")

        assert result.files_created == []
        assert "ya existe" in result.message


def test_validate_valid_skill() -> None:
    """Validate should return valid=True for a properly structured skill."""
    with tempfile.TemporaryDirectory() as tmpdir:
        creator = SkillCreateSkill(skills_dir=tmpdir)
        creator.scaffold(skill_name="valid_skill", description="Valid")
        validation = creator.validate(str(Path(tmpdir) / "valid_skill"))

        assert validation.valid is True
        assert validation.skill_name == "valid_skill"
        assert validation.missing_files == []
        assert validation.errors == []


def test_validate_missing_files() -> None:
    """Validate should report missing files for an incomplete skill."""
    with tempfile.TemporaryDirectory() as tmpdir:
        skill_path = Path(tmpdir) / "incomplete_skill"
        skill_path.mkdir()
        (skill_path / "__init__.py").write_text('"""Incomplete skill."""\n')

        creator = SkillCreateSkill(skills_dir=tmpdir)
        validation = creator.validate(str(skill_path))

        assert validation.valid is False
        assert "skill.py" in validation.missing_files
        assert "README.md" in validation.missing_files
        assert len(validation.errors) > 0


def test_validate_nonexistent_path() -> None:
    """Validate should return valid=False for a non-existent path."""
    creator = SkillCreateSkill(skills_dir="/tmp/nonexistent")
    validation = creator.validate("/tmp/nonexistent/does_not_exist")

    assert validation.valid is False
    assert validation.skill_name is None
    assert "no existe" in validation.errors[0]


def test_list_skills() -> None:
    """List should return all skills in the directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        creator = SkillCreateSkill(skills_dir=tmpdir)
        creator.scaffold(skill_name="alpha_skill", description="Alpha")
        creator.scaffold(skill_name="beta_skill", description="Beta")

        skills = creator.list_skills()
        assert skills.total == 2
        names = {s["name"] for s in skills.skills}
        assert names == {"alpha_skill", "beta_skill"}


def test_generate_file_content() -> None:
    """generate_file should return content without writing to disk."""
    creator = SkillCreateSkill(skills_dir="/tmp")
    gen = creator.generate_file(
        skill_name="my_skill",
        file_type="config",
        description="My skill config",
    )

    assert gen.file_type == "config"
    assert "API_BASE_URL" in gen.content
    assert gen.target_path.endswith("/my_skill/config.py") or gen.target_path.endswith(
        "skills/my_skill/config.py"
    )


def test_class_name_convention() -> None:
    """Generated __init__.py should export the correct class name."""
    with tempfile.TemporaryDirectory() as tmpdir:
        creator = SkillCreateSkill(skills_dir=tmpdir)
        creator.scaffold(skill_name="web_search", description="Web search")

        init_content = Path(tmpdir, "web_search", "__init__.py").read_text(
            encoding="utf-8"
        )
        assert "from .skill import WebSearchSkill" in init_content
        assert "__all__ = [\"WebSearchSkill\"]" in init_content


def test_readme_has_title() -> None:
    """Generated README should have a main title."""
    with tempfile.TemporaryDirectory() as tmpdir:
        creator = SkillCreateSkill(skills_dir=tmpdir)
        creator.scaffold(skill_name="doc_skill", description="Docs")

        readme = Path(tmpdir, "doc_skill", "README.md").read_text(encoding="utf-8")
        assert "# Doc Skill" in readme or "# doc_skill Skill" in readme