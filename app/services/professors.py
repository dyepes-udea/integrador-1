from pandas import DataFrame
from sqlalchemy.orm import Session

from app.repositories.postgresql.crud import ProfessorCRUD
from app.repositories.postgresql.tables import Professor as ProfessorTable
from app.schemas.programs import Program
from app.schemas.projects import ProjectRol
from app.services.professors_programs import professor_program_service
from app.services.professors_projects import professor_project_service
from app.schemas.errors import MassiCreationError
from app.schemas.professors import (
    CreateProfessor,
    MassiCreationResult,
    Professor,
    ProfessorFilters,
)


class ProfessorService:
    def __init__(self) -> None:
        self.__crud = ProfessorCRUD(table=ProfessorTable)

    def get_all(
        self, *, session: Session, filters: ProfessorFilters,
    ) -> list[Professor]:
        professors = self.__crud.get_all(
            session=session,
            skip=filters.skip,
            limit=filters.limit,
            filters=filters.model_dump(
                exclude={"skip", "limit"}, exclude_defaults=True,
            ),
        )
        return [Professor.model_validate(professor) for professor in professors]
    
    def get_by_identification_number(
        self, *, session: Session, identification_number: str,
    ) -> Professor:
        professor = self.__crud.get_by_identification_number(
            session=session, identification_number=identification_number,
        )
        return Professor.model_validate(professor)
    
    def get_programs(
        self, *, session: Session, identification_number: str,
    ) -> list[Program]:
        professor = self.get_by_identification_number(
            session=session, identification_number=identification_number,
        )
        return professor_program_service.get_programs_by_professor_id(
            session=session, professor_id=professor.id,
        )
    
    def get_projects(
        self, *, session: Session, identification_number: str,
    ) -> list[ProjectRol]:
        professor = self.get_by_identification_number(
            session=session, identification_number=identification_number,
        )
        return professor_project_service.get_projects_by_professor_id(
            session=session, professor_id=professor.id,
        )

    def create(
        self, *, session: Session, new_professor: CreateProfessor,
    ) -> Professor:
        professor = self.__crud.create(session=session, model=new_professor)
        return Professor.model_validate(professor)
    
    def create_per_dataframe(
        self, *, session: Session, data: DataFrame,
    ) -> MassiCreationResult:
        errors = []
        professors = []
        for i, row in data.iterrows():
            try:
                new_professor = CreateProfessor(
                    identification_number=row["Numero de identificación"],
                    identification_type=row["Tipo de identificación"],
                    full_name=row["Nombre"],
                    gender=row["Sexo"],
                    contract_type=row["Tipo de vinculación"],
                    employment_class=row["Tipo de contrato"],
                    institutional_email=row["Email institucional"],
                )
                professor = self.create(
                    session=session, new_professor=new_professor,
                )
                professors.append(professor)
            except Exception as e:
                errors.append(MassiCreationError(row=i+1, error=str(e)))
        return MassiCreationResult(professors=professors, errors=errors)


professor_service = ProfessorService()
