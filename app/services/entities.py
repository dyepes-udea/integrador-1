from sqlalchemy.orm import Session

from app.repositories.postgresql.crud import EntityCRUD
from app.repositories.postgresql.tables import Entity as EntityTable
from app.schemas.entities import CreateEntity, Entity


class EntityService:
    def __init__(self) -> None:
        self.__crud = EntityCRUD(table=EntityTable)

    def get_or_create(
        self, *, session: Session, code: int, new_entity: CreateEntity,
    ) -> Entity:
        entity = self.__crud.get_or_create(
            session=session, code=code, new_entity=new_entity,
        )
        return Entity.model_validate(entity)
    
    def get_by_code(self, *, session: Session, code: int) -> Entity:
        program = self.__crud.get_by_code(session=session, code=code)
        return Entity.model_validate(program)


entity_service = EntityService()
