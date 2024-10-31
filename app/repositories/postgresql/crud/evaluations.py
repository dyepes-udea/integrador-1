from app.repositories.postgresql.crud.base import BaseCRUD
from app.repositories.postgresql.tables import Evaluation as EvaluationTable
from app.schemas.evaluations import Evaluation as EvaluationModel


class EvaluationCRUD(BaseCRUD[EvaluationTable, EvaluationModel]):
    ...
