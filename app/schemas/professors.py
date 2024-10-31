from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

from app.schemas.errors import MassiCreationError
from app.schemas.professors_projects import RoleEnum


FILE_FORMAT: list[str] = [
    "Numero de identificación",
    "Tipo de identificación",
    "Nombre",
    "Sexo",
    "Tipo de vinculación",
    "Tipo de contrato",
    "Email institucional",
]


class IdentificationTypeEnum(str, Enum):
    CC = "Cédula de ciudadanía"
    CE = "Cédula de extranjería"
    PASSPORT = "Pasaporte"


class GenderEnum(str, Enum):
    EMPTY = ""
    MALE = "Hombre"
    FEMALE = "Mujer"


class ContractTypeEnum(str, Enum):
    DOCAT = "Docente de catedra"
    DOCEN = "Docente"


class EmploymentClassEnum(str, Enum):
    ASPIR = "Aspirante"
    OCASI = "Ocasional"
    EXTER = "Externo"
    REGUL = "Regular"
    EMPLENODOCENTE = "Empleado no docente"


class CreateProfessor(BaseModel):
    identification_number: str = Field(..., max_length=20)
    identification_type: IdentificationTypeEnum = ...
    full_name: str = ...
    gender: GenderEnum = GenderEnum.EMPTY
    contract_type: ContractTypeEnum = ...
    employment_class: EmploymentClassEnum = ...
    institutional_email: EmailStr | None = None

    @field_validator("full_name")
    def full_name_to_title(cls, v: str) -> Any:
        return v.title()
    
    @field_validator("identification_number", mode="before")
    def identification_number_to_str(cls, v: Any) -> str:
        return str(v)
    
    @field_validator("institutional_email", mode="before")
    def allow_empty_email(cls, v: Any) -> Any:
        if v == "":
            return None
        return v


class Professor(CreateProfessor):
    id: int = ...

    model_config = ConfigDict(from_attributes=True)


class ProfessorRol(Professor):
    role: RoleEnum = ...


class ProfessorFilters(BaseModel):
    skip: int = 0
    limit: int = 100
    gender: GenderEnum | None = None
    contract_type: ContractTypeEnum | None = None
    employment_class: EmploymentClassEnum | None = None


class MassiCreationResult(BaseModel):
    professors: list[Professor] = ...
    errors: list[MassiCreationError] = ...
