from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from pandas import DataFrame
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.api.endpoints.dependencies.database import get_db
from app.api.endpoints.dependencies.dataframe import file_to_dataframe
from app.schemas.admissions import (
    FILE_FORMAT,
    Admission,
    AdmissionFilters,
    CreateAdmission,
    MassiCreationResult,
)
from app.services.admissions import admission_service


router = APIRouter()


@router.get(
    "",
    response_model=list[Admission],
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Admissions found"},
    }
)
def get_all(
    filters: Annotated[AdmissionFilters, Query()],
    session: Annotated[Session, Depends(get_db)],
):
    try:
        admissions = admission_service.get_all(session=session, filters=filters)
        return admissions
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Program not found"
        )


@router.post(
    "",
    response_model=Admission,
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Admission Created"},
        404: {"description": "Program not found"},
    }
)
def create(
    new_admission: CreateAdmission,
    session: Annotated[Session, Depends(get_db)],
):
    try:
        admission = admission_service.create(
            session=session, new_admission=new_admission,
        )
        return admission
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Program not found"
        )


@router.post(
    "/file",
    response_model=MassiCreationResult,
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Admission Created"},
    }
)
def create_per_file(
    data: Annotated[DataFrame, Depends(file_to_dataframe(FILE_FORMAT))],
    session: Annotated[Session, Depends(get_db)],
):
    result = admission_service.create_per_dataframe(
        session=session, data=data,
    )
    return result
