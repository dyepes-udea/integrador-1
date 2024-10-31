from pandas import DataFrame
from sqlalchemy.orm import Session

from app.repositories.postgresql.crud import SubjectCRUD
from app.repositories.postgresql.tables import Subject as SubjectTable
from app.schemas.errors import MassiCreationError
from app.schemas.subjects import (
    SubjectFilters,
    CreateSubject,
    Subject,
    MassiCreationResult,
)


class SubjectService:
    def __init__(self) -> None:
        self.__crud = SubjectCRUD(table=SubjectTable)

    def get_all(
        self, *, session: Session, filters: SubjectFilters,
    ) -> list[Subject]:
        subjects = self.__crud.get_all(
            session=session,
            skip=filters.skip,
            limit=filters.limit,
            filters=filters.model_dump(
                exclude={"skip", "limit"}, exclude_defaults=True,
            ),
        )
        return [Subject.model_validate(subject) for subject in subjects]
    
    def get_by_code(self, *, session: Session, code: int) -> Subject:
        program = self.__crud.get_by_code(session=session, code=code)
        return Subject.model_validate(program)
    
    def create(
        self, *, session: Session, new_subject: CreateSubject,
    ) -> Subject:
        subject = self.__crud.create(session=session, model=new_subject)
        return Subject.model_validate(subject)
    
    def create_per_dataframe(
        self, *, session: Session, data: DataFrame,
    ) -> MassiCreationResult:
        errors = []
        subjects = []
        for i, row in data.iterrows():
            try:
                new_subject = CreateSubject(
                    code=row["Código"],
                    name=row["Nombre"],
                    credits=row["Créditos"],
                    is_enabled=row["Habilitable"],
                    study_plan_version=row["Versión pensum"],
                    description=row["Descripción"],
                )
                subject = self.create(
                    session=session, new_subject=new_subject,
                )
                subjects.append(subject)
            except Exception as e:
                errors.append(MassiCreationError(row=i+1, error=str(e)))
        return MassiCreationResult(subjects=subjects, errors=errors)


subject_service = SubjectService()
