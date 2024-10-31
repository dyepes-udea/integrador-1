from pandas import DataFrame
from sqlalchemy.orm import Session

from app.repositories.postgresql.crud import AdmissionCRUD
from app.repositories.postgresql.tables import Admission as AdmissionTable
from app.schemas.errors import MassiCreationError
from app.services.programs import program_service
from app.schemas.admissions import (
    AdmissionFilters,
    CreateAdmission,
    Admission,
    InCreateAdmission,
    MassiCreationResult,
)


class AdmissionService:
    def __init__(self) -> None:
        self.__crud = AdmissionCRUD(table=AdmissionTable)

    def get_all(
        self, *, session: Session, filters: AdmissionFilters,
    ) -> list[Admission]:
        new_fielters = filters.model_dump(
            exclude={"skip", "limit", "program_code"},
            exclude_defaults=True,
        )

        if filters.program_code:
            program = program_service.get_by_code(
                session=session, code=filters.program_code,
            )
            new_fielters["program_id"] = program.id

        admissions = self.__crud.get_all(
            session=session,
            skip=filters.skip,
            limit=filters.limit,
            filters=new_fielters,
        )
        return [Admission.model_validate(admission) for admission in admissions]
    
    def create(
        self, *, session: Session, new_admission: CreateAdmission,
    ) -> Admission:
        program = program_service.get_by_code(
            session=session,
            code=new_admission.program_code,
        )
        admission = self.__crud.create(
            session=session,
            model=InCreateAdmission(
                program_id=program.id,
                **new_admission.model_dump(exclude={"program_code"}),
            ),
        )
        return Admission.model_validate(admission)
    
    def create_per_dataframe(
        self, *, session: Session, data: DataFrame,
    ) -> MassiCreationResult:
        errors = []
        admissions = []
        for i, row in data.iterrows():
            try:
                new_admission = CreateAdmission(
                    semester=row["Semestre"],
                    year=row["Año"],
                    admitted_students=row["Admitidos"],
                    transfer_admitted_students=row["Traslado"],
                    reentry_admitted_students=row["Reingreso"],
                    enrolled_students=row["Matriculados"],
                    program_code=row["Programa"],
                )
                admission = self.create(
                    session=session, new_admission=new_admission,
                )
                admissions.append(admission)
            except Exception as e:
                errors.append(MassiCreationError(row=i+1, error=str(e)))
        return MassiCreationResult(admissions=admissions, errors=errors)


admission_service = AdmissionService()
