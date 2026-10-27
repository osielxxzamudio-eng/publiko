"""Configuration for the Skill Create skill (skill scaffolder)."""

import os

SKILLS_DIR = os.getenv("SKILLS_DIR", "skills")

SKILL_FILES = [
    "__init__.py",
    "config.py",
    "models.py",
    "client.py",
    "skill.py",
    "README.md",
]

SKILL_TEMPLATE_VARS = {
    "skill_name": "Nombre de la skill en PascalCase",
    "skill_description": "Descripción breve de la skill",
    "skill_version": "1.0.0",
}

REQUEST_TIMEOUT_SECONDS = 30