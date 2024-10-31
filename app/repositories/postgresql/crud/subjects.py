from typing import Any

from sqlalchemy.orm import Session

from app.repositories.postgresql.crud.base import BaseCRUD
from app.repositories.postgresql.tables import Subject as SubjectTable
from app.schemas.subjects import Subject as SubjectModel


class SubjectCRUD(BaseCRUD[SubjectTable, SubjectModel]):
    def get_by_code(self, *, session: Session, code: int) -> SubjectTable:
        return session.query(self._table) \
            .filter(self._table.code == code) \
            .one()

    def get_all(
        self,
        *,
        session: Session,
        skip: int,
        limit: int,
        filters: dict[str, Any],
    ) -> list[SubjectModel]:
        query = session.query(self._table)
        if filters:
            for key, value in filters.items():
                if key == "study_plan_version":
                    query = query.filter(
                        self._table.study_plan_version.any(value)
                    )
                else:
                    query = query.filter(getattr(self._table, key) == value)
        return query.offset(skip).limit(limit).all()
