from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from fastapi.responses import JSONResponse
from pandas import DataFrame
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.api.endpoints.dependencies.database import get_db
from app.api.endpoints.dependencies.dataframe import file_to_dataframe
from app.schemas.professors import ProfessorRol
from app.schemas.projects import (
    FILE_FORMAT,
    Project,
    CreateProject,
    MassiCreationResult,
    ProjectFilters,
)
from app.services.projects import project_service


router = APIRouter()


@router.get(
    "",
    response_model=list[Project],
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Projects found"},
    }
)
def get_all(
    filters: Annotated[ProjectFilters, Query()],
    session: Annotated[Session, Depends(get_db)],
):
    projects = project_service.get_all(session=session, filters=filters)
    return projects


@router.post(
    "",
    response_model=Project,
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Project Created"},
    }
)
def create(
    new_project: CreateProject,
    session: Annotated[Session, Depends(get_db)],
):
    project = project_service.create(
        session=session, new_project=new_project,
    )
    return project


@router.post(
    "/file",
    response_model=MassiCreationResult,
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Project Created"},
    }
)
def create_per_file(
    data: Annotated[DataFrame, Depends(file_to_dataframe(FILE_FORMAT))],
    session: Annotated[Session, Depends(get_db)],
):
    result = project_service.create_per_dataframe(
        session=session, data=data,
    )
    return result


@router.get(
    "/{code}/professors",
    response_model=list[ProfessorRol],
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
        professors = project_service.get_professors(
            session=session, code=code,
        )
        return professors
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
