from sqlalchemy.orm import Session

from app.repositories.postgresql.crud.base import BaseCRUD
from app.repositories.postgresql.tables import Program as ProgramTable
from app.schemas.programs import Program as ProgramModel


class ProgramCRUD(BaseCRUD[ProgramTable, ProgramModel]):
    def get_by_code(self, *, session: Session, code: int) -> ProgramTable:
        return session.query(self._table) \
            .filter(self._table.code == code) \
            .one()
