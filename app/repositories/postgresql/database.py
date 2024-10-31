from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from app.config import settings
from app.logger import get_logger


logger = get_logger()


class PostgreSQL:
    def __init__(self) -> None:
        self.__base = declarative_base()
        self.__engine = create_engine(settings.postgresql.unicode_string())
        self.__session_local = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.__engine,
        )
    
    def base(self) -> Any:
        return self.__base
    
    def session(self) -> Session:
        return self.__session_local()
    
    def create_tables(self) -> None:
        from . import tables

        logger.info("Creating tables...")
        self.__base.metadata.create_all(bind=self.__engine)
        logger.info("Successfully created tables")


postgresql = PostgreSQL()
