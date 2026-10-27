"""Data models for the Skill Verification skill requests and responses."""

from typing import Any, Optional
from pydantic import BaseModel, Field


class SkillCheckResult(BaseModel):
    """Resultado de la verificación de una skill individual."""

    skill_name: str = Field(..., description="Nombre de la skill verificada")
    skill_path: str = Field(..., description="Ruta al directorio de la skill")
    valid: bool = Field(..., description="Si la skill pasa todas las verificaciones")
    missing_files: list[str] = Field(default_factory=list, description="Archivos requeridos faltantes")
    errors: list[str] = Field(default_factory=list, description="Errores críticos encontrados")
    warnings: list[str] = Field(default_factory=list, description="Advertencias no críticas")
    import_ok: bool = Field(default=False, description="Si el import de la skill funciona")
    structure_ok: bool = Field(default=False, description="Si la estructura de archivos es correcta")
    readme_ok: bool = Field(default=False, description="Si el README tiene las secciones requeridas")


class VerifyAllResponse(BaseModel):
    """Respuesta de verificación de todas las skills."""

    total_skills: int = Field(..., description="Número total de skills encontradas")
    valid_skills: int = Field(..., description="Número de skills válidas")
    invalid_skills: int = Field(..., description="Número de skills inválidas")
    results: list[SkillCheckResult] = Field(default_factory=list, description="Resultado por skill")
    all_valid: bool = Field(..., description="Si todas las skills son válidas")
    summary: str = Field(..., description="Resumen legible de la verificación")


class VerifySkillResponse(BaseModel):
    """Respuesta de verificación de una skill individual."""

    skill_name: str
    valid: bool
    missing_files: list[str]
    errors: list[str]
    warnings: list[str]
    import_ok: bool
    structure_ok: bool
    readme_ok: bool


class RepositoryHealthResponse(BaseModel):
    """Respuesta del estado de salud del repositorio."""

    healthy: bool = Field(..., description="Si el repositorio está saludable")
    total_skills: int
    valid_skills: int
    invalid_skills: int
    issues: list[str] = Field(default_factory=list, description="Issues encontrados en el repositorio")
    recommendations: list[str] = Field(default_factory=list, description="Recomendaciones de mejora")