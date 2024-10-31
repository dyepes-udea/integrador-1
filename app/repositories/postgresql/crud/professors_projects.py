from typing import Any

from sqlalchemy.orm import Session

from app.repositories.postgresql.crud.base import BaseCRUD
from app.repositories.postgresql.tables import (
    ProfessorProject as ProfessorProjectTable,
    Project as ProjectTable,
    Professor as ProfessorTable,
)
from app.schemas.professors_projects import ProfessorProject as ProfessorProjectModel


class ProfessorProjectCRUD(BaseCRUD[ProfessorProjectTable, ProfessorProjectModel]):
    def get_professors_by_project_id(
        self, *, session: Session, project_id: int,
    ) -> list[ProfessorTable]:
        professor_projects = session.query(self._table) \
            .join(ProfessorTable) \
            .filter(self._table.project_id == project_id) \
            .all()
        return [
            {
                **prof_project.professor.__dict__.copy(),
                "role": prof_project.role,
            }
            for prof_project in professor_projects
        ]
    
    def get_projects_by_professor_id(
        self, *, session: Session, professor_id: int,
    ) -> list[dict[str, Any]]:
        professor_projects = session.query(self._table) \
            .join(ProjectTable) \
            .filter(self._table.professor_id == professor_id) \
            .all()
        return [
            {
                **prof_project.project.__dict__.copy(),
                "role": prof_project.role,
            }
            for prof_project in professor_projects
        ]
