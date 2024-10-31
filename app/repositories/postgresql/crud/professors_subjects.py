from app.repositories.postgresql.crud.base import BaseCRUD
from app.repositories.postgresql.tables import ProfessorSubject as ProfessorSubjectTable
from app.schemas.professors_subjects import ProfessorSubject as ProfessorSubjectModel


class ProfessorSubjectCRUD(BaseCRUD[ProfessorSubjectTable, ProfessorSubjectModel]):
    ...
