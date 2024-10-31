from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator

from app.schemas.errors import MassiCreationError


FILE_FORMAT: list[str] = [
    "Código",
    "Nombre",
    "Créditos",
    "Habilitable",
    "Versión pensum",
    "Descripción",
]


class CreateSubject(BaseModel):
    code: int = ...
    name: str = ...
    credits: int = ...
    is_enabled: bool = ...
    study_plan_version: set[int] = ...
    description: str | None = None

    @field_validator("name")
    def name_to_title(cls, v: str) -> Any:
        return v.title()

    @field_validator("study_plan_version", mode="before")
    def study_plan_version_to_set_str(cls, v: Any) -> set[str] | Any:
        if type(v) == str:
            return set(v.split(","))
        return v


class Subject(CreateSubject):
    id: int = ...

    model_config = ConfigDict(from_attributes=True)


class SubjectFilters(BaseModel):
    skip: int = 0
    limit: int = 100
    is_enabled: bool | None = None
    study_plan_version: int | None = None


class MassiCreationResult(BaseModel):
    subjects: list[Subject] = ...
    errors: list[MassiCreationError] = ...
