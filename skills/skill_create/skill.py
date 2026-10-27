"""Skill Create — high-level interface for scaffolding new skills in the pubblico repository."""

import os
from pathlib import Path
from typing import Any

from .config import SKILL_FILES, SKILLS_DIR
from .models import (
    GenerateFileResponse,
    SkillListResponse,
    SkillScaffoldResponse,
    SkillValidateResponse,
)


class SkillCreateSkill:
    """Skill para crear y scafflear nuevas skills en el repositorio pubblico."""

    def __init__(self, skills_dir: str | None = None) -> None:
        self.skills_dir = Path(skills_dir or SKILLS_DIR)

    def scaffold(
        self,
        skill_name: str,
        description: str,
        version: str = "1.0.0",
        author: str | None = None,
    ) -> SkillScaffoldResponse:
        skill_path = self.skills_dir / skill_name

        if skill_path.exists():
            return SkillScaffoldResponse(
                skill_name=skill_name,
                skill_path=str(skill_path),
                files_created=[],
                message=f"La skill '{skill_name}' ya existe en {skill_path}",
            )

        skill_path.mkdir(parents=True, exist_ok=True)

        files_created: list[str] = []

        for file_name in SKILL_FILES:
            if file_name.endswith(".md"):
                file_type = "readme"
            elif file_name.endswith(".py"):
                file_type = file_name[:-3]  # quitar .py
            else:
                file_type = file_name

            content = self._generate_file_content(
                skill_name=skill_name,
                file_type=file_type,
                description=description,
                version=version,
                author=author,
            )
            target_file = skill_path / file_name
            target_file.write_text(content, encoding="utf-8")
            files_created.append(str(target_file))

        return SkillScaffoldResponse(
            skill_name=skill_name,
            skill_path=str(skill_path),
            files_created=files_created,
            message=f"La skill '{skill_name}' creada exitosamente en {skill_path}",
        )

    def validate(self, skill_path: str) -> SkillValidateResponse:
        """Validar que una skill siga el patrón correcto del repositorio."""
        path = Path(skill_path)

        if not path.exists():
            return SkillValidateResponse(
                valid=False,
                skill_name=None,
                missing_files=list(SKILL_FILES),
                errors=[f"La ruta '{skill_path}' no existe"],
                warnings=[],
            )

        missing_files_set: set[str] = set()
        errors: list[str] = []
        warnings: list[str] = []

        for required_file in SKILL_FILES:
            if not (path / required_file).exists():
                missing_files_set.add(required_file)

        init_file = path / "__init__.py"
        if init_file.exists():
            init_content = init_file.read_text(encoding="utf-8")
            skill_name = path.name
            expected_class = "".join(word.capitalize() for word in skill_name.split("_")) + "Skill"
            if f"from .skill import {expected_class}" not in init_content:
                warnings.append(
                    f"__init__.py no exporta la clase esperada '{expected_class}'"
                )
        else:
            missing_files_set.add("__init__.py")

        skill_file = path / "skill.py"
        if skill_file.exists():
            skill_content = skill_file.read_text(encoding="utf-8")
            if "class " not in skill_content:
                errors.append("skill.py no contiene ninguna clase definida")
        else:
            missing_files_set.add("skill.py")
            errors.append("skill.py no se encuentra")

        readme_file = path / "README.md"
        if not readme_file.exists():
            missing_files_set.add("README.md")
        else:
            readme_content = readme_file.read_text(encoding="utf-8")
            if "# " not in readme_content:
                warnings.append("README.md no tiene un título principal (#)")

        missing_files = sorted(missing_files_set)
        valid = len(missing_files) == 0 and len(errors) == 0

        skill_name = path.name if path.exists() else None

        return SkillValidateResponse(
            valid=valid,
            skill_name=skill_name,
            missing_files=missing_files,
            errors=errors,
            warnings=warnings,
        )

    def list_skills(self) -> SkillListResponse:
        """Listar todas las skills disponibles en el directorio skills/."""
        skills: list[dict[str, Any]] = []

        if not self.skills_dir.exists():
            return SkillListResponse(skills=[], total=0)

        for entry in sorted(self.skills_dir.iterdir()):
            if not entry.is_dir():
                continue

            validation = self.validate(str(entry))
            skills.append(
                {
                    "name": entry.name,
                    "path": str(entry),
                    "valid": validation.valid,
                    "missing_files": validation.missing_files,
                    "warnings": validation.warnings,
                }
            )

        return SkillListResponse(skills=skills, total=len(skills))

    def generate_file(
        self,
        skill_name: str,
        file_type: str,
        description: str | None = None,
    ) -> GenerateFileResponse:
        """Generar el contenido de un archivo individual de skill sin escribirlo en disco."""
        target_path = str(self.skills_dir / skill_name / f"{file_type}.py")
        if file_type == "readme":
            target_path = str(self.skills_dir / skill_name / "README.md")

        content = self._generate_file_content(
            skill_name=skill_name,
            file_type=file_type,
            description=description or f"Skill {skill_name}",
        )

        return GenerateFileResponse(
            file_type=file_type,
            content=content,
            target_path=target_path,
        )

    def _generate_file_content(
        self,
        skill_name: str,
        file_type: str,
        description: str,
        version: str = "1.0.0",
        author: str | None = None,
    ) -> str:
        """Generar el contenido de un archivo de skill basado en su tipo."""
        class_name = "".join(word.capitalize() for word in skill_name.split("_")) + "Skill"

        if file_type == "__init__":
            return (
                f'"""{{skill_description}}."""\n\n'
                f"from .skill import {class_name}\n\n"
                f'__all__ = ["{class_name}"]\n'
                f'__version__ = "{version}"\n'
            ).replace("{{skill_description}}", description)

        if file_type == "config":
            return (
                f'"""Configuration for the {skill_name} skill."""\n\n'
                "import os\n\n"
                'API_BASE_URL = os.getenv("API_BASE_URL", "https://api.example.com")\n'
                'API_KEY = os.getenv("API_KEY", "")\n'
                'API_AUTH_HEADER = "x-api-key"\n\n'
                'ENDPOINT = "/endpoint"\n\n'
                "DEFAULT_NUM_RESULTS = 10\n"
                'DEFAULT_MODE = "auto"\n\n'
                "REQUEST_TIMEOUT_SECONDS = 30\n"
            )

        if file_type == "models":
            return (
                f'"""Data models for the {skill_name} skill requests and responses."""\n\n'
                "from typing import Any, Optional\n"
                "from pydantic import BaseModel, Field\n\n"
                f"\n\nclass {class_name}Request(BaseModel):\n"
                f'    """Request model for the {skill_name} skill."""\n\n'
                '    query: str = Field(..., description="Query string")\n'
                '    num_results: int = Field(default=10, ge=1, le=100, description="Number of results")\n\n'
                f"\n\nclass {class_name}Result(BaseModel):\n"
                f'    """A single result item."""\n\n'
                "    title: str\n    url: str\n    score: Optional[float] = None\n\n"
                f"\n\nclass {class_name}Response(BaseModel):\n"
                f'    """Response model for the {skill_name} skill."""\n\n'
                "    query: str\n"
                f"    results: list[{class_name}Result]\n"
                "    total_results: int\n"
                '    raw: dict[str, Any] = Field(default_factory=dict)\n'
            )

        if file_type == "client":
            return (
                f'"""HTTP client for the API used by the {skill_name} skill."""\n\n'
                "from typing import Any\n\n"
                "import httpx\n\n"
                'from .config import API_AUTH_HEADER, API_BASE_URL, API_KEY, ENDPOINT, REQUEST_TIMEOUT_SECONDS\n\n\n'
                "class ExampleClient:\n"
                '    """Async HTTP client for the API."""\n\n'
                "    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:\n"
                "        self.api_key = api_key or API_KEY\n"
                "        self.base_url = base_url or API_BASE_URL\n"
                "        self._client: httpx.AsyncClient | None = None\n\n"
                "    async def __aenter__(self) -> \"ExampleClient\":\n"
                "        headers = {API_AUTH_HEADER: self.api_key}\n"
                "        self._client = httpx.AsyncClient(\n"
                "            base_url=self.base_url,\n"
                "            headers=headers,\n"
                "            timeout=REQUEST_TIMEOUT_SECONDS,\n"
                "        )\n"
                "        return self\n\n"
                "    async def __aexit__(self, *args: Any) -> None:\n"
                "        if self._client:\n"
                "            await self._client.aclose()\n\n"
                "    async def endpoint(self, query: str, num_results: int = 10) -> dict[str, Any]:\n"
                '        """Call the API endpoint."""\n'
                "        if not self._client:\n"
                '            raise RuntimeError("ExampleClient must be used as an async context manager")\n\n'
                '        payload: dict[str, Any] = {"query": query, "num_results": num_results}\n\n'
                "        response = await self._client.post(ENDPOINT, json=payload)\n"
                "        response.raise_for_status()\n"
                "        return response.json()\n"
            )

        if file_type == "skill":
            return (
                f'"""{{skill_name}} skill — high-level interface for the API."""\n\n'
                "from typing import Any\n\n"
                "from .client import ExampleClient\n"
                f"from .config import DEFAULT_NUM_RESULTS, DEFAULT_MODE\n"
                f"from .models import (\n"
                f"    {class_name}Request,\n"
                f"    {class_name}Response,\n"
                f"    {class_name}Result,\n"
                f")\n\n\n"
                f"class {class_name}:\n"
                f'    """Skill para {description} usando la API."""\n\n'
                "    def __init__(self, api_key: str | None = None, base_url: str | None = None) -> None:\n"
                "        self.api_key = api_key\n"
                "        self.base_url = base_url\n\n"
                "    async def search(\n"
                "        self,\n"
                "        query: str,\n"
                "        num_results: int = DEFAULT_NUM_RESULTS,\n"
                "        mode: str = DEFAULT_MODE,\n"
                "    ) -> Response:\n"
                '        """Buscar y retornar resultados estructurados."""\n'
                "        request = Request(\n"
                "            query=query,\n"
                "            num_results=num_results,\n"
                "        )\n\n"
                "        async with ExampleClient(api_key=self.api_key, base_url=self.base_url) as client:\n"
                "            data = await client.endpoint(\n"
                "                query=request.query,\n"
                "                num_results=request.num_results,\n"
                "            )\n\n"
                "        results = [\n"
                "            Result(\n"
                "                title=item.get(\"title\", \"\"),\n"
                "                url=item.get(\"url\", \"\"),\n"
                "                score=item.get(\"score\"),\n"
                "            )\n"
                "            for item in data.get(\"results\", [])\n"
                "        ]\n\n"
                "        return Response(\n"
                "            query=request.query,\n"
                "            results=results,\n"
                "            total_results=len(results),\n"
                "            raw=data,\n"
                "        )\n"
            ).replace("{{skill_name}}", skill_name).replace("Response", f"{class_name}Response").replace("Request", f"{class_name}Request").replace("Result", f"{class_name}Result")

        if file_type == "readme":
            return (
                f"# {skill_name} Skill\n\n"
                f"Skill para {description} usando la API.\n\n"
                "## Operaciones\n\n"
                "| Operación | Descripción |\n"
                "|-----------|-------------|\n"
                "| search | Búsqueda general |\n\n"
                "## Instalación\n\n"
                "```bash\n"
                "pip install -r requirements.txt\n"
                "```\n\n"
                "## Configuración\n\n"
                "```bash\n"
                'export API_KEY="tu-api-key-aqui"\n'
                "```\n\n"
                "## Uso\n\n"
                "```python\n"
                "import asyncio\n"
                f"from skills.{skill_name} import {class_name}\n\n\n"
                "async def main() -> None:\n"
                f"    skill = {class_name}()\n\n"
                '    response = await skill.search(\n'
                '        query="ejemplo de consulta",\n'
                "        num_results=5,\n"
                "    )\n"
                '    for r in response.results:\n'
                '        print(f"- {r.title}: {r.url}")\n\n\n'
                "asyncio.run(main())\n"
                "```\n\n"
                "## Requerimientos\n\n"
                "- Python 3.10+\n"
                "- `httpx`\n"
                "- `pydantic`\n\n"
                "## Licencia\n\n"
                "[Especificar licencia]\n"
            )

        return f"# {file_type}\n\nPlaceholder for {skill_name}\n"