from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from app.schemas.health_check import HealthCheck
from app.services.health_check import health_check_service


router = APIRouter()


@router.get(
    "",
    response_model=HealthCheck,
    response_class=JSONResponse,
    status_code=status.HTTP_200_OK,
    responses={
        200: {"description": "Health status of the revised api"},
    }
)
def health_check():
    status = health_check_service.get_status()
    return status
