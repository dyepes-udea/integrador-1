from enum import Enum

from pydantic import BaseModel, ConfigDict


class RoleEnum(str, Enum):
    ADVISOR = "Asesor"
    ASSISTANT_INVESTIGATOR = "Auxiliar de investigación"
    CO_INVESTIGATOR = "Coinvestigador"
    PROJECT_COORDINATOR = "Coordinador del proyecto"
    GRADUATE = "Egresado"
    UNDERGRADUATE_STUDENT = "Estudiante de pregrado"
    DOCTORAL_STUDENT = "Estudiante en formación (Doctorado)"
    MASTERS_STUDENT = "Estudiante en formación (Maestría)"
    PRINCIPAL_INVESTIGATOR = "Investigador principal"
    YOUNG_INVESTIGATOR = "Jóven investigador"
    OTHER_ROLES = "Otros roles"


class CreateProfessorProject(BaseModel):
    professor_id: int = ...
    project_id: int = ...
    role: RoleEnum = ...


class ProfessorProject(CreateProfessorProject):
    model_config = ConfigDict(from_attributes=True)
