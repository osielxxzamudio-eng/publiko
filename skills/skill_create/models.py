"""Data models for the Skill Create skill requests and responses."""

from typing import Any, Optional
from pydantic import BaseModel, Field


class SkillScaffoldRequest(BaseModel):
    """Request to scaffold a new skill."""

    skill_name: str = Field(..., description="Name of the new skill (snake_case, e.g. web_search)")
    description: str = Field(..., description="Brief description of what the skill does")
    version: str = Field(default="1.0.0", description="Initial version of the skill")
    author: Optional[str] = Field(default=None, description="Author of the skill")


class SkillScaffoldResponse(BaseModel):
    """Response after scaffolding a skill."""

    skill_name: str
    skill_path: str
    files_created: list[str]
    message: str


class SkillValidateRequest(BaseModel):
    """Request to validate an existing skill."""

    skill_path: str = Field(..., description="Path to the skill directory to validate")


class SkillValidateResponse(BaseModel):
    """Response from skill validation."""

    valid: bool
    skill_name: Optional[str]
    missing_files: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


class SkillListResponse(BaseModel):
    """Response listing all available skills."""

    skills: list[dict[str, Any]]
    total: int


class GenerateFileRequest(BaseModel):
    """Request to generate a single skill file."""

    skill_name: str = Field(..., description="Name of the skill")
    file_type: str = Field(..., description="Type of file to generate: init, config, models, client, skill, readme")
    description: Optional[str] = Field(default=None, description="Description for the skill")


class GenerateFileResponse(BaseModel):
    """Response with generated file content."""

    file_type: str
    content: str
    target_path: str