from sqlalchemy.orm import Session

from app.repositories.postgresql.crud.base import BaseCRUD
from app.repositories.postgresql.tables import (
    Professor as ProfessorTable,
    Program as ProgramTable,
    ProfessorProgram as ProfessorProgramTable,
)
from app.schemas.professors_programs import ProfessorProgram as ProfessorProgramModel


class ProfessorProgramCRUD(BaseCRUD[ProfessorProgramTable, ProfessorProgramModel]):
    def get_professors_by_program_id(
        self, *, session: Session, program_id: int,
    ) -> list[ProfessorTable]:
        professor_programs = session.query(self._table) \
            .join(ProfessorTable) \
            .filter(self._table.program_id == program_id) \
            .all()
        return [prof_program.professor for prof_program in professor_programs]

    def get_programs_by_professor_id(
        self, *, session: Session, professor_id: int,
    ) -> list[ProgramTable]:
        professor_programs = session.query(self._table) \
            .join(ProgramTable) \
            .filter(self._table.professor_id == professor_id) \
            .all()
        return [prof_program.program for prof_program in professor_programs]
