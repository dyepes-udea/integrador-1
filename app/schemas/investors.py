from enum import Enum

from pydantic import BaseModel, ConfigDict

from app.schemas.errors import MassiCreationError


FILE_FORMAT: list[str] = [
    "Tipo",
    "Total fresco",
    "Total en especie",
    "Código del aportante",
    "Aportante",
    "Proyecto",
]


class TypeEnum(str, Enum):
    CO_FUNDER = "Cofinanciador"
    FUNDER = "Financiador"


class BaseInvestor(BaseModel):
    type: TypeEnum = ...
    amount: int = ...
    kind: int = ...


class CreateInvestor(BaseInvestor):
    project_code: int = ...
    entity_code: int = ...
    entity_name: str = ...


class InCreateInvestor(BaseInvestor):
    project_id: int = ...
    entity_id: int = ...


class Investor(InCreateInvestor):
    id: int = ...

    model_config = ConfigDict(from_attributes=True)


class InvestorFilters(BaseModel):
    skip: int = 0
    limit: int = 100
    project_code: int | None = None
    entity_code: int | None = None


class MassiCreationResult(BaseModel):
    investors: list[Investor] = ...
    errors: list[MassiCreationError] = ...
