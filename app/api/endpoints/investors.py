from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse
from pandas import DataFrame
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound

from app.api.endpoints.dependencies.database import get_db
from app.api.endpoints.dependencies.dataframe import file_to_dataframe
from app.schemas.investors import (
    FILE_FORMAT,
    Investor,
    InvestorFilters,
    CreateInvestor,
    MassiCreationResult,
)
from app.services.investors import investor_service


router = APIRouter()


@router.get(
    "",
    response_model=list[Investor],
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Investors found"},
    }
)
def get_all(
    filters: Annotated[InvestorFilters, Query()],
    session: Annotated[Session, Depends(get_db)],
):
    try:
        investors = investor_service.get_all(session=session, filters=filters)
        return investors
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project or entity not found"
        )


@router.post(
    "",
    response_model=Investor,
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Investor Created"},
        404: {"description": "Investor not found"},
    }
)
def create(
    new_investor: CreateInvestor,
    session: Annotated[Session, Depends(get_db)],
):
    try:
        investor = investor_service.create(
            session=session, new_investor=new_investor,
        )
        return investor
    except NoResultFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Investor not found"
        )


@router.post(
    "/file",
    response_model=MassiCreationResult,
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Investor Created"},
    }
)
def create_per_file(
    data: Annotated[DataFrame, Depends(file_to_dataframe(FILE_FORMAT))],
    session: Annotated[Session, Depends(get_db)],
):
    result = investor_service.create_per_dataframe(
        session=session, data=data,
    )
    return result
