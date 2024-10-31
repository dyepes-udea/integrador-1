from sqlalchemy.orm import Session

from app.repositories.postgresql.crud.base import BaseCRUD
from app.repositories.postgresql.tables import Professor as ProfessorTable
from app.schemas.professors import CreateProfessor as ProfessorModel


class ProfessorCRUD(BaseCRUD[ProfessorTable, ProfessorModel]):
    def get_by_identification_number(
        self, *, session: Session, identification_number: str,
    ) -> ProfessorTable:
        return session.query(self._table) \
            .filter(self._table.identification_number == identification_number) \
            .one()
