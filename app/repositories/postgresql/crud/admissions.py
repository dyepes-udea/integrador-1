from app.repositories.postgresql.crud.base import BaseCRUD
from app.repositories.postgresql.tables import Admission as AdmissionTable
from app.schemas.admissions import Admission as AdmissionModel


class AdmissionCRUD(BaseCRUD[AdmissionTable, AdmissionModel]):
    ...
