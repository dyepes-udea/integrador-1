from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import JSONResponse
from pandas import DataFrame
from sqlalchemy.orm import Session

from app.api.endpoints.dependencies.database import get_db
from app.api.endpoints.dependencies.dataframe import file_to_dataframe
from app.schemas.subjects import (
    FILE_FORMAT,
    Subject,
    SubjectFilters,
    CreateSubject,
    MassiCreationResult,
)
from app.services.subjects import subject_service


router = APIRouter()


@router.get(
    "",
    response_model=list[Subject],
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Subjects found"},
    }
)
def get_all(
    filters: Annotated[SubjectFilters, Query()],
    session: Annotated[Session, Depends(get_db)],
):
    subjects = subject_service.get_all(session=session, filters=filters)
    return subjects


@router.post(
    "",
    response_model=Subject,
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Subject Created"},
    }
)
def create(
    new_subject: CreateSubject,
    session: Annotated[Session, Depends(get_db)],
):
    subject = subject_service.create(
        session=session, new_subject=new_subject,
    )
    return subject


@router.post(
    "/file",
    response_model=MassiCreationResult,
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Subject Created"},
    }
)
def create_per_file(
    data: Annotated[DataFrame, Depends(file_to_dataframe(FILE_FORMAT))],
    session: Annotated[Session, Depends(get_db)],
):
    result = subject_service.create_per_dataframe(
        session=session, data=data,
    )
    return result
