"""Configuration for the Skill Verification skill."""

import os

SKILLS_DIR = os.getenv("SKILLS_DIR", "skills")

REQUIRED_FILES = [
    "__init__.py",
    "config.py",
    "models.py",
    "client.py",
    "skill.py",
    "README.md",
]

REQUIRED_CLASSES_PATTERN = {
    "__init__.py": "from .skill import",
    "skill.py": "class ",
}

REQUIRED_README_SECTIONS = [
    "# ",
    "## Instalación",
    "## Uso",
]

VERIFICATION_TIMEOUT_SECONDS = 30