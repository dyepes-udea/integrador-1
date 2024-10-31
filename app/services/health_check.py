from app.config import settings
from app.schemas.health_check import HealthCheck, Status


class HealthCheckService:
    def get_status(self) -> HealthCheck:
        return HealthCheck(
            title=settings.title,
            status=Status.ok,
            version=settings.version,
            environment=settings.environment,
        )


health_check_service = HealthCheckService()
