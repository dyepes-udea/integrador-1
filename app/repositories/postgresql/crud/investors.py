from app.repositories.postgresql.crud.base import BaseCRUD
from app.repositories.postgresql.tables import Investor as InvestorTable
from app.schemas.investors import Investor as InvestorModel


class InvestorCRUD(BaseCRUD[InvestorTable, InvestorModel]):
    ...
