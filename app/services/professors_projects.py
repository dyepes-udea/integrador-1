from sqlalchemy.orm import Session

from app.repositories.postgresql.crud import ProfessorProjectCRUD
from app.repositories.postgresql.tables import ProfessorProject as ProfessorProjectTable
from app.schemas.professors import ProfessorRol
from app.schemas.professors_projects import (
    CreateProfessorProject,
    ProfessorProject,
)
from app.schemas.projects import ProjectRol


class ProfessorProjectService:
    def __init__(self) -> None:
        self.__crud = ProfessorProjectCRUD(table=ProfessorProjectTable)

    def get_professors_by_project_id(
        self, *, session: Session, project_id: int,
    ) -> list[ProfessorRol]:
        professors = self.__crud.get_professors_by_project_id(
            session=session, project_id=project_id,
        )
        return [ProfessorRol.model_validate(professor) for professor in professors]

    def get_projects_by_professor_id(
        self, *, session: Session, professor_id: int,
    ) -> list[ProjectRol]:
        projects = self.__crud.get_projects_by_professor_id(
            session=session, professor_id=professor_id,
        )
        return [ProjectRol.model_validate(project) for project in projects]

    def create(
        self,
        *,
        session: Session,
        new_professor_project: CreateProfessorProject,
    ) -> ProfessorProject:
        professor_project = self.__crud.create(
            session=session, model=new_professor_project,
        )
        return ProfessorProject.model_validate(professor_project)


professor_project_service = ProfessorProjectService()
