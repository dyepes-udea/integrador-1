from pandas import DataFrame
from sqlalchemy.orm import Session

from app.repositories.postgresql.crud import ProfessorSubjectCRUD
from app.repositories.postgresql.tables import ProfessorSubject as ProfessorSubjectTable
from app.schemas.errors import MassiCreationError
from app.services.professors import professor_service
from app.services.subjects import subject_service
from app.schemas.professors_subjects import (
    ProfessorSubjectFilters,
    CreateProfessorSubject,
    ProfessorSubject,
    InCreateProfessorSubject,
    MassiCreationResult,
)


class ProfessorSubjectService:
    def __init__(self) -> None:
        self.__crud = ProfessorSubjectCRUD(table=ProfessorSubjectTable)

    def get_all(
        self, *, session: Session, filters: ProfessorSubjectFilters,
    ) -> list[ProfessorSubject]:
        new_fielters = filters.model_dump(
            exclude={
                "skip",
                "limit",
                "professor_identification_number",
                "subject_code",
            },
            exclude_defaults=True,
        )

        if filters.professor_identification_number:
            professor = professor_service.get_by_identification_number(
                session=session,
                identifier=filters.professor_identification_number,
            )
            new_fielters["professor_id"] = professor.id
        if filters.subject_code:
            subject = subject_service.get_by_code(
                session=session,
                code=filters.subject_code,
            )
            new_fielters["subject_id"] = subject.id

        professors_subjects = self.__crud.get_all(
            session=session,
            skip=filters.skip,
            limit=filters.limit,
            filters=new_fielters,
        )
        return [
            ProfessorSubject.model_validate(professor_subject)
            for professor_subject in professors_subjects
        ]
    
    def create(
        self, *, session: Session, new_professor_subject: CreateProfessorSubject,
    ) -> ProfessorSubject:
        professor = professor_service.get_by_identification_number(
            session=session,
            identification_number=new_professor_subject.professor_identification_number,
        )
        subject = subject_service.get_by_code(
            session=session, code=new_professor_subject.subject_code,
        )

        professor_subject = self.__crud.create(
            session=session,
            model=InCreateProfessorSubject(
                professor_id=professor.id,
                subject_id=subject.id,
                **new_professor_subject.model_dump(
                    exclude={
                        "professor_identification_number",
                        "subject_code",
                    },
                ),
            ),
        )
        return ProfessorSubject.model_validate(professor_subject)
    
    def create_per_dataframe(
        self, *, session: Session, data: DataFrame,
    ) -> MassiCreationResult:
        errors = []
        professors_subjects = []
        for i, row in data.iterrows():
            try:
                new_professor_subject = CreateProfessorSubject(
                    professor_identification_number=row["Profesor"],
                    subject_code=row["Materia"],
                    semester=row["Semestre"],
                    year=row["Año"],
                    group=row["Grupo"],
                    location=row["Ubicación"],
                    available_spots=row["Cupos"],
                    enrolled_students=row["Matriculados"],
                    cancelled_students=row["Cancelaciones"],
                    missed_students=row["Perdieron"],
                    avg_note=row["avg nota"],
                    stddev_note=row["stddev nota"],

                )
                professor_subject = self.create(
                    session=session,
                    new_professor_subject=new_professor_subject,
                )
                professors_subjects.append(professor_subject)
            except Exception as e:
                errors.append(MassiCreationError(row=i+1, error=str(e)))
        return MassiCreationResult(professors_subjects=professors_subjects, errors=errors)


professor_subject_service = ProfessorSubjectService()
