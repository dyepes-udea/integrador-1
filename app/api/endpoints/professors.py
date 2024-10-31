from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi.responses import JSONResponse
from pandas import DataFrame
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.api.endpoints.dependencies.database import get_db
from app.api.endpoints.dependencies.dataframe import file_to_dataframe
from app.schemas.professors import (
    FILE_FORMAT,
    CreateProfessor,
    MassiCreationResult,
    Professor,
    ProfessorFilters,
)
from app.schemas.programs import Program
from app.schemas.projects import ProjectRol
from app.services.professors import professor_service


router = APIRouter()


@router.get(
    "",
    response_model=list[Professor],
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Professors found"},
    }
)
def get_all(
    filters: Annotated[ProfessorFilters, Query()],
    session: Annotated[Session, Depends(get_db)],
):
    professors = professor_service.get_all(session=session, filters=filters)
    return professors


@router.post(
    "",
    response_model=Professor,
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Professor Created"},
    }
)
def create(
    new_professor: CreateProfessor,
    session: Annotated[Session, Depends(get_db)],
):
    professor = professor_service.create(
        session=session, new_professor=new_professor,
    )
    return professor


@router.post(
    "/file",
    response_model=MassiCreationResult,
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Professors Created"},
    }
)
def create_per_file(
    data: Annotated[DataFrame, Depends(file_to_dataframe(FILE_FORMAT))],
    session: Annotated[Session, Depends(get_db)],
):
    result = professor_service.create_per_dataframe(
        session=session, data=data,
    )
    return result


@router.get(
    "/{identification_number}/programs",
    response_model=list[Program],
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Programs"},
        404: {"description": "Professor not found"},
    }
)
def get_programs(
    identification_number: Annotated[str, Path(max_length=20)],
    session: Annotated[Session, Depends(get_db)],
):
    try:
        programs = professor_service.get_programs(
            session=session, identification_number=identification_number,
        )
        return programs
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professor not found"
        )


@router.get(
    "/{identification_number}/projects",
    response_model=list[ProjectRol],
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Projects"},
        404: {"description": "Professor not found"},
    }
)
def get_programs(
    identification_number: Annotated[str, Path(max_length=20)],
    session: Annotated[Session, Depends(get_db)],
):
    try:
        projects = professor_service.get_projects(
            session=session, identification_number=identification_number,
        )
        return projects
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professor not found"
        )
