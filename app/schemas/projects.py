from datetime import date
from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator

from app.schemas.errors import MassiCreationError
from app.schemas.professors_projects import RoleEnum


FILE_FORMAT: list[str] = [
    "Código",
    "Nombre",
    "Estado",
    "Convocatoria",
    "Fecha de inicio",
    "Fecha de finalización",
    "Profesor",
    "Rol",
]


class StatusEnum(str, Enum):
    APPROVED = "Aprobado"
    IN_PROGRESS = "En Ejecución"
    COMPLETED = "Finalizado"
    SETTLED = "Liquidado"
    PENDING_PROGRAMMED = "Pendiente de Programación"


class BaseProject(BaseModel):
    code: int = ...
    name: str = ...
    status: StatusEnum = ...
    call: str = ...
    start_date: date = ...
    end_date: date | None = None

    @field_validator("name", "call")
    def name_call_to_title(cls, v: str) -> Any:
        return v.title()


class CreateProject(BaseProject):
    professor: str = ...
    role: RoleEnum = ...

    @field_validator("professor", mode="before")
    def professor_to_str(cls, v: Any) -> str:
        return str(v)
    
    def model_dump(self, **kwargs):
        kwargs.setdefault("exclude", set())
        kwargs["exclude"].add("professor")
        kwargs["exclude"].add("role")
        return super().model_dump(**kwargs)


class Project(BaseProject):
    id: int = ...
    members: list[dict[str, Any]] = ...

    model_config = ConfigDict(from_attributes=True)


class ProjectRol(Project):
    role: RoleEnum = ...


class ProjectFilters(BaseModel):
    skip: int = 0
    limit: int = 100
    call: str | None = None
    status: StatusEnum | None = None


class MassiCreationResult(BaseModel):
    projects: list[Project] = ...
    errors: list[MassiCreationError] = ...
