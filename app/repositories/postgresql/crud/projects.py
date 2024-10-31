from sqlalchemy.orm import Session

from app.repositories.postgresql.crud.base import BaseCRUD
from app.repositories.postgresql.tables import Project as ProjectTable
from app.schemas.projects import Project as ProjectModel


class ProjectCRUD(BaseCRUD[ProjectTable, ProjectModel]):
    def get_by_code(self, *, session: Session, code: int) -> ProjectTable:
        return session.query(self._table) \
            .filter(self._table.code == code) \
            .one()
