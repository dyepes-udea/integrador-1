from pydantic import BaseModel, ConfigDict

from app.schemas.errors import MassiCreationError


FILE_FORMAT: list[str] = [
    "Programa",
    "Semestre",
    "Año",
    "Admitidos",
    "Traslado",
    "Reingreso",
    "Matriculados",
]


class BaseAdmission(BaseModel):
    semester: int = ...
    year: int = ...
    admitted_students: int = ...
    transfer_admitted_students: int = ...
    reentry_admitted_students: int = ...
    enrolled_students: int = ...


class CreateAdmission(BaseAdmission):
    program_code: int = ...


class InCreateAdmission(BaseAdmission):
    program_id: int = ...


class Admission(InCreateAdmission):
    id: int = ...

    model_config = ConfigDict(from_attributes=True)


class AdmissionFilters(BaseModel):
    skip: int = 0
    limit: int = 100
    year: int | None = None
    program_code: int | None = None


class MassiCreationResult(BaseModel):
    admissions: list[Admission] = ...
    errors: list[MassiCreationError] = ...
