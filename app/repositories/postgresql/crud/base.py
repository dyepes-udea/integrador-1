from typing import Any, Type, TypeVar, Generic

from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.repositories.postgresql.tables.base import Base


T = TypeVar("T", bound=Base)
C = TypeVar("C", bound=BaseModel)


class BaseCRUD(Generic[T, C]):
    def __init__(self, *, table: Type[T]) -> None:
        self._table = table
    
    def create(self, *, session: Session, model: C) -> T:
        try:
            db_obj = self._table(**model.model_dump())
            session.add(db_obj)
            session.commit()
            session.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            session.rollback()
            raise e

    def get(self, *, session: Session, obj_id: int) -> T | None:
        return session.get(self._table, obj_id)
    
    def get_all(
        self,
        *,
        session: Session,
        skip: int,
        limit: int,
        filters: dict[str, Any],
    ) -> list[T]:
        query = session.query(self._table)
        if filters:
            for key, value in filters.items():
                query = query.filter(getattr(self._table, key) == value)
        return query.offset(skip).limit(limit).all()
    
    def update(self, *, session: Session, obj_id: int, model: dict[str, Any]) -> None:
        try:
            db_obj = self.get(session=session, obj_id=obj_id)
            if not db_obj:
                return None

            for column, value in model.items():
                setattr(db_obj, column, value)

            session.commit()
            session.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            session.rollback()
            raise e
    
    def delete(self, *, session: Session, obj_id: int) -> None:
        try:
            db_obj = self.get(session=session, obj_id=obj_id)
            if not db_obj:
                return None

            session.delete(db_obj)
            session.commit()
            return db_obj
        except SQLAlchemyError as e:
            session.rollback()
            raise e
