from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse
from pandas import DataFrame
from sqlalchemy.orm import Session

from app.api.endpoints.dependencies.database import get_db
from app.api.endpoints.dependencies.dataframe import file_to_dataframe
from app.schemas.professors_subjects import (
    FILE_FORMAT,
    ProfessorSubject,
    ProfessorSubjectFilters,
    CreateProfessorSubject,
    MassiCreationResult,
)
from app.services.professors_subjects import professor_subject_service


router = APIRouter()


@router.get(
    "",
    response_model=list[ProfessorSubject],
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Professors Subjects found"},
    }
)
def get_all(
    filters: Annotated[ProfessorSubjectFilters, Query()],
    session: Annotated[Session, Depends(get_db)],
):
    professors_professor_subjects = professor_subject_service.get_all(session=session, filters=filters)
    return professors_professor_subjects


@router.post(
    "",
    response_model=ProfessorSubject,
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Professor Subject Created"},
    }
)
def create(
    new_professor_subject: CreateProfessorSubject,
    session: Annotated[Session, Depends(get_db)],
):
    professor_subject = professor_subject_service.create(
        session=session, new_professor_subject=new_professor_subject,
    )
    return professor_subject


@router.post(
    "/file",
    response_model=MassiCreationResult,
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Professor Subject Created"},
    }
)
def create_per_file(
    data: Annotated[DataFrame, Depends(file_to_dataframe(FILE_FORMAT))],
    session: Annotated[Session, Depends(get_db)],
):
    result = professor_subject_service.create_per_dataframe(
        session=session, data=data,
    )
    return result
