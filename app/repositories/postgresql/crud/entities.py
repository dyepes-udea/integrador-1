from sqlalchemy.orm import Session

from app.repositories.postgresql.crud.base import BaseCRUD
from app.repositories.postgresql.tables import Entity as EntityTable
from app.schemas.entities import CreateEntity, Entity as EntityModel


class EntityCRUD(BaseCRUD[EntityTable, EntityModel]):
    def get_by_code(self, *, session: Session, code: int) -> EntityTable:
        return session.query(self._table) \
            .filter(self._table.code == code) \
            .one()

    def get_or_create(
        self, *, session: Session, code: int, new_entity: CreateEntity,
    ) -> EntityTable:
        entity = session.query(self._table) \
            .filter(self._table.code == code) \
            .first()
        
        if entity:
            return entity
        
        return self.create(session=session, model=new_entity)
