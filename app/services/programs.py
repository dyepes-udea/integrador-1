from pandas import DataFrame
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.repositories.postgresql.crud import ProgramCRUD
from app.repositories.postgresql.tables import Program as ProgramTable
from app.schemas.professors import Professor
from app.schemas.professors_programs import CreateProfessorProgram
from app.schemas.programs_subjects import CreateProgramSubject
from app.schemas.subjects import Subject
from app.services.professors import professor_service
from app.services.subjects import subject_service
from app.services.professors_programs import professor_program_service
from app.services.programs_subjects import program_subject_service
from app.services.programs_subjects import program_subject_service
from app.schemas.errors import MassiCreationError
from app.schemas.programs import (
    CreateProgram,
    MassiCreationResult,
    Program,
    ProgramFilters,
)


class ProgramService:
    def __init__(self) -> None:
        self.__crud = ProgramCRUD(table=ProgramTable)

    def get_all(
        self, *, session: Session, filters: ProgramFilters,
    ) -> list[Program]:
        programs = self.__crud.get_all(
            session=session,
            skip=filters.skip,
            limit=filters.limit,
            filters=filters.model_dump(
                exclude={"skip", "limit"}, exclude_defaults=True,
            ),
        )
        return [Program.model_validate(program) for program in programs]
    
    def get_by_code(self, *, session: Session, code: int) -> Program:
        program = self.__crud.get_by_code(session=session, code=code)
        return Program.model_validate(program)
    
    def get_professors(self, *, session: Session, code: int) -> list[Professor]:
        program = self.get_by_code(session=session, code=code)
        return professor_program_service.get_professors_by_program_id(
            session=session, program_id=program.id,
        )
    
    def get_subjects(self, *, session: Session, code: int) -> list[Subject]:
        program = self.get_by_code(session=session, code=code)
        return program_subject_service.get_subjects_by_program_id(
            session=session, program_id=program.id,
        )
    
    def __create_professors_program(
        self, *, session: Session, program_id: int, professors: set[str],
    ) -> None:
        for identification_number in professors:
            try:
                professor = professor_service.get_by_identification_number(
                    session=session,
                    identification_number=identification_number,
                )
            except NoResultFound:
                continue
            professor_program_service.create(
                session=session,
                new_professor_program=CreateProfessorProgram(
                    professor_id=professor.id,
                    program_id=program_id,
                ),
            )

    def __create_program_subjects(
        self, *, session: Session, program_id: int, subjects: set[str],
    ) -> None:
        for code in subjects:
            try:
                subject = subject_service.get_by_code(
                    session=session, code=code,
                )
            except NoResultFound:
                continue
            program_subject_service.create(
                session=session,
                new_program_subject=CreateProgramSubject(
                    subject_id=subject.id,
                    program_id=program_id,
                ),
            )

    def create(
        self, *, session: Session, new_program: CreateProgram,
    ) -> Program:
        program = self.__crud.create(session=session, model=new_program)
        self.__create_professors_program(
            session=session,
            program_id=program.id,
            professors=new_program.professors,
        )
        self.__create_program_subjects(
            session=session,
            program_id=program.id,
            subjects=new_program.subjects,
        )
        return Program.model_validate(program)
    
    def create_per_dataframe(
        self, *, session: Session, data: DataFrame,
    ) -> MassiCreationResult:
        errors = []
        programs = []
        for i, row in data.iterrows():
            try:
                new_program = CreateProgram(
                    code=row["Código"],
                    name=row["Nombre"],
                    type=row["Tipo"],
                    modality=row["Modalidad"],
                    professors=row["Profesores"],
                    subjects=row["Materias"],
                )
                program = self.create(
                    session=session, new_program=new_program,
                )
                programs.append(program)
            except Exception as e:
                errors.append(MassiCreationError(row=i+1, error=str(e)))
        return MassiCreationResult(programs=programs, errors=errors)


program_service = ProgramService()
