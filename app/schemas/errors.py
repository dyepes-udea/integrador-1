from pydantic import BaseModel


class MassiCreationError(BaseModel):
    row: int = ...
    error: str = ...
