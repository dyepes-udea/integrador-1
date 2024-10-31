from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator

from app.schemas.errors import MassiCreationError


FILE_FORMAT: list[str] = [
    "Nombre",
    "Código",
    "Tipo",
    "Modalidad",
    "Profesores",
    "Materias",
]


class TypeEnum(str, Enum):
    UNDERGRADUATE = "Pregrado"
    SPECIALISATION = "Especialización"
    MASTER_DEGREE = "Maestria"
    DOCTORATE = "Doctorado"


class ModalityEnum(str, Enum):
    PRESENCIAL = "Presencial"
    VIRTUAL = "Virtual"


class BaseProgram(BaseModel):
    code: int = ...
    name: str = ...
    type: TypeEnum = ...
    modality: ModalityEnum = ...

    @field_validator("name")
    def name_to_title(cls, v: str) -> Any:
        return v.title()


class CreateProgram(BaseProgram):
    professors: set[str] = ...
    subjects: set[str] = ...

    @field_validator("professors", "subjects", mode="before")
    def professors_to_set_str(cls, v: Any) -> set[str] | Any:
        if type(v) == str:
            return set(v.split(","))
        return v
    
    def model_dump(self, **kwargs):
        kwargs.setdefault("exclude", set())
        kwargs["exclude"].add("professors")
        kwargs["exclude"].add("subjects")
        return super().model_dump(**kwargs)


class Program(BaseProgram):
    id: int = ...

    model_config = ConfigDict(from_attributes=True)


class ProgramFilters(BaseModel):
    skip: int = 0
    limit: int = 100
    type: TypeEnum | None = None
    modality: ModalityEnum | None = None


class MassiCreationResult(BaseModel):
    programs: list[Program] = ...
    errors: list[MassiCreationError] = ...
