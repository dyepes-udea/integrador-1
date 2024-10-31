from sqlalchemy.orm import Session

from app.repositories.postgresql.crud import ProfessorProgramCRUD
from app.repositories.postgresql.tables import ProfessorProgram as ProfessorProgramTable
from app.schemas.professors import Professor
from app.schemas.professors_programs import (
    CreateProfessorProgram,
    ProfessorProgram,
)
from app.schemas.programs import Program


class ProfessorProgramService:
    def __init__(self) -> None:
        self.__crud = ProfessorProgramCRUD(table=ProfessorProgramTable)

    def get_professors_by_program_id(
        self, *, session: Session, program_id: int,
    ) -> list[Professor]:
        professors = self.__crud.get_professors_by_program_id(
            session=session, program_id=program_id,
        )
        return [Professor.model_validate(professor) for professor in professors]

    def get_programs_by_professor_id(
        self, *, session: Session, professor_id: int,
    ) -> list[Program]:
        programs = self.__crud.get_programs_by_professor_id(
            session=session, professor_id=professor_id,
        )
        return [Program.model_validate(program) for program in programs]
        
    def create(
        self,
        *,
        session: Session,
        new_professor_program: CreateProfessorProgram,
    ) -> ProfessorProgram:
        professor_program = self.__crud.create(
            session=session, model=new_professor_program,
        )
        return ProfessorProgram.model_validate(professor_program)


professor_program_service = ProfessorProgramService()
