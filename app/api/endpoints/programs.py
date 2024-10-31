from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi.responses import JSONResponse
from pandas import DataFrame
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.api.endpoints.dependencies.database import get_db
from app.api.endpoints.dependencies.dataframe import file_to_dataframe
from app.schemas.professors import Professor
from app.schemas.programs import (
    FILE_FORMAT,
    CreateProgram,
    MassiCreationResult,
    Program,
    ProgramFilters,
)
from app.schemas.subjects import Subject
from app.services.programs import program_service


router = APIRouter()


@router.get(
    "",
    response_model=list[Program],
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Programs found"},
    }
)
def get_all(
    filters: Annotated[ProgramFilters, Query()],
    session: Annotated[Session, Depends(get_db)],
):
    programs = program_service.get_all(session=session, filters=filters)
    return programs


@router.post(
    "",
    response_model=Program,
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Program Created"},
    }
)
def create(
    new_program: CreateProgram,
    session: Annotated[Session, Depends(get_db)],
):
    professor = program_service.create(
        session=session, new_program=new_program,
    )
    return professor


@router.post(
    "/file",
    response_model=MassiCreationResult,
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Programs Created"},
    }
)
def create_per_file(
    data: Annotated[DataFrame, Depends(file_to_dataframe(FILE_FORMAT))],
    session: Annotated[Session, Depends(get_db)],
):
    result = program_service.create_per_dataframe(
        session=session, data=data,
    )
    return result


@router.get(
    "/{code}/professors",
    response_model=list[Professor],
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Professors"},
        404: {"description": "Program not found"},
    }
)
def get_professors(
    code: Annotated[int, Path()],
    session: Annotated[Session, Depends(get_db)],
):
    try:
        professors = program_service.get_professors(
            session=session, code=code,
        )
        return professors
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Program not found"
        )


@router.get(
    "/{code}/subjects",
    response_model=list[Subject],
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Subjects"},
        404: {"description": "Program not found"},
    }
)
def get_subjects(
    code: Annotated[int, Path()],
    session: Annotated[Session, Depends(get_db)],
):
    try:
        subjects = program_service.get_subjects(
            session=session, code=code,
        )
        return subjects
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Program not found"
        )
