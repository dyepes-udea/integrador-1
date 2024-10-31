from sqlalchemy.orm import Session

from app.repositories.postgresql.crud import ProgramSubjectCRUD
from app.repositories.postgresql.tables import ProgramSubject as ProgramSubjectTable
from app.schemas.subjects import Subject
from app.schemas.programs_subjects import (
    CreateProgramSubject,
    ProgramSubject,
)
from app.schemas.programs import Program


class ProgramSubjectService:
    def __init__(self) -> None:
        self.__crud = ProgramSubjectCRUD(table=ProgramSubjectTable)

    def get_subjects_by_program_id(
        self, *, session: Session, program_id: int,
    ) -> list[Subject]:
        subjects = self.__crud.get_subjects_by_program_id(
            session=session, program_id=program_id,
        )
        return [Subject.model_validate(subject) for subject in subjects]

    def get_programs_by_subject_id(
        self, *, session: Session, subject_id: int,
    ) -> list[Program]:
        programs = self.__crud.get_programs_by_subject_id(
            session=session, subject_id=subject_id,
        )
        return [Program.model_validate(program) for program in programs]
        
    def create(
        self,
        *,
        session: Session,
        new_program_subject: CreateProgramSubject,
    ) -> ProgramSubject:
        program_subject = self.__crud.create(
            session=session, model=new_program_subject,
        )
        return ProgramSubject.model_validate(program_subject)


program_subject_service = ProgramSubjectService()
