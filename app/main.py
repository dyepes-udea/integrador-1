from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api
from app.config import settings
from app.logger import get_logger
from app.repositories.postgresql.database import postgresql


logger = get_logger()


def on_startup() -> None:
    postgresql.create_tables()


def on_shutdown() -> None:
    ...


app = FastAPI(
    title=settings.title,
    description=settings.description,
    version=settings.version,
    on_startup=[on_startup],
    on_shutdown=[on_shutdown],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(api.router, prefix="/api")
