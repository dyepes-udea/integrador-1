from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.schemas.errors import MassiCreationError


FILE_FORMAT: list[str] = [
    "Profesor",
    "Materia",
    "Semestre",
    "Año",
    "Grupo",
    "Ubicación",
    "Cupos",
    "Matriculados",
    "Cancelaciones",
    "Perdieron",
    "avg nota",
    "stddev nota",
]


class LocationEnum(str, Enum):
    INGENIA = "Ingenia"
    CLASSROOM = "Salón"
    UDEARROBA = "Ude@"
    INGENIA_CLASSROOM = "Ingenia y Salón"
    UDEARROBA_CLASSEROOM = "Ude@ y Salón"


class BaseProfessorSubject(BaseModel):
    semester: int = ...
    year: int = ...
    group: int = ...
    location: LocationEnum = ...
    available_spots: int = ...
    enrolled_students: int = ...
    cancelled_students: int = ...
    missed_students: int = ...
    avg_note: float = ...
    stddev_note: float = ...


class CreateProfessorSubject(BaseProfessorSubject):
    professor_identification_number: str = Field(..., max_length=20)
    subject_code: int = ...

    @field_validator("professor_identification_number", mode="before")
    def identification_number_to_str(cls, v: Any) -> str:
        return str(v)


class InCreateProfessorSubject(BaseProfessorSubject):
    professor_id: int = ...
    subject_id: int = ...


class ProfessorSubject(InCreateProfessorSubject):
    id: int = ...

    model_config = ConfigDict(from_attributes=True)


class ProfessorSubjectFilters(BaseModel):
    skip: int = 0
    limit: int = 100
    professor_identification_number: str | None = Field(None, max_length=20)
    subject_code: int | None = None
    semester: int | None = None
    year: int | None = None


class MassiCreationResult(BaseModel):
    professors_subjects: list[ProfessorSubject] = ...
    errors: list[MassiCreationError] = ...
