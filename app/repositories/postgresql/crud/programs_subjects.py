from sqlalchemy.orm import Session

from app.repositories.postgresql.crud.base import BaseCRUD
from app.repositories.postgresql.tables import (
    Program as ProgramTable,
    Subject as SubjectTable,
    ProgramSubject as ProgramSubjectTable,
)
from app.schemas.programs_subjects import ProgramSubject as ProgramSubjectModel


class ProgramSubjectCRUD(BaseCRUD[ProgramSubjectTable, ProgramSubjectModel]):
    def get_subjects_by_program_id(
        self, *, session: Session, program_id: int,
    ) -> list[SubjectTable]:
        program_subjects = session.query(self._table) \
            .join(SubjectTable) \
            .filter(self._table.program_id == program_id) \
            .all()
        return [
            program_subject.subject
            for program_subject in program_subjects
        ]

    def get_programs_by_subject_id(
        self, *, session: Session, subject_id: int,
    ) -> list[ProgramTable]:
        program_subjects = session.query(self._table) \
            .join(ProgramTable) \
            .filter(self._table.subject_id == subject_id) \
            .all()
        return [
            program_subject.program
            for program_subject in program_subjects
        ]
