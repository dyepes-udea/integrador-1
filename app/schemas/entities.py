from pydantic import BaseModel, ConfigDict


class CreateEntity(BaseModel):
    code: int = ...
    name: str = ...


class Entity(CreateEntity):
    id: int = ...

    model_config = ConfigDict(from_attributes=True)
