from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship

from app.repositories.postgresql.database import postgresql


class Entity(postgresql.base()):
    __tablename__ = "entities"

    id = Column(Integer, primary_key=True)
    code = Column(Integer, nullable=False, unique=True)
    name = Column(Text, nullable=False)

    investors = relationship("Investor", back_populates="entity")
