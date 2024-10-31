from pandas import DataFrame
from sqlalchemy.orm import Session

from app.repositories.postgresql.crud import ProjectCRUD
from app.repositories.postgresql.tables import Project as ProjectTable
from app.schemas.professors import ProfessorRol
from app.schemas.professors_projects import CreateProfessorProject
from app.services.professors import professor_service
from app.services.professors_projects import professor_project_service
from app.schemas.errors import MassiCreationError
from app.schemas.projects import (
    CreateProject,
    Project,
    MassiCreationResult,
    ProjectFilters,
)


class ProjectService:
    def __init__(self) -> None:
        self.__crud = ProjectCRUD(table=ProjectTable)

    def get_all(
        self, *, session: Session, filters: ProjectFilters,
    ) -> list[Project]:
        subjects = self.__crud.get_all(
            session=session,
            skip=filters.skip,
            limit=filters.limit,
            filters=filters.model_dump(
                exclude={"skip", "limit"}, exclude_defaults=True,
            ),
        )
        return [Project.model_validate(subject) for subject in subjects]
    
    def get_by_code(self, *, session: Session, code: int) -> Project:
        project = self.__crud.get_by_code(session=session, code=code)
        return Project.model_validate(project)
    
    def get_professors(self, *, session: Session, code: int) -> list[ProfessorRol]:
        project = self.get_by_code(session=session, code=code)
        return professor_project_service.get_professors_by_project_id(
            session=session, project_id=project.id,
        )

    def create(
        self, *, session: Session, new_project: CreateProject,
    ) -> Project:
        project = self.__crud.create(session=session, model=new_project)
        professor = professor_service.get_by_identification_number(
            session=session,
            identification_number=new_project.professor,
        )
        professor_project_service.create(
            session=session,
            new_professor_project=CreateProfessorProject(
                professor_id=professor.id,
                project_id=project.id,
                role=new_project.role,
            ),
        )
        return Project.model_validate(project)
    
    def create_per_dataframe(
        self, *, session: Session, data: DataFrame,
    ) -> MassiCreationResult:
        errors = []
        projects = []
        for i, row in data.iterrows():
            try:
                new_project = CreateProject(
                    code=row["Código"],
                    name=row["Nombre"],
                    status=row["Estado"],
                    call=row["Convocatoria"],
                    start_date=row["Fecha de inicio"],
                    end_date=row["Fecha de finalización"],
                    professor=row["Profesor"],
                    role=row["Rol"],
                )
                project = self.create(
                    session=session, new_project=new_project,
                )
                projects.append(project)
            except Exception as e:
                errors.append(MassiCreationError(row=i+1, error=str(e)))
        return MassiCreationResult(projects=projects, errors=errors)


project_service = ProjectService()
