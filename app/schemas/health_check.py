from enum import Enum

from pydantic import BaseModel


class Status(str, Enum):
    ok = "OK"
    failure = "FAILURE"


class HealthCheck(BaseModel):
    title: str = ...
    status: Status = ...
    version: str = ...
    environment: str = ...
