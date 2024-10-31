from sqlalchemy import Column, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.repositories.postgresql.database import postgresql


class Investor(postgresql.base()):
    __tablename__ = "investors"
    
    id = Column(Integer, primary_key=True)
    type = Column(
        Enum(
            "Cofinanciador",
            "Financiador",
            name="investor_type",
        ),
        nullable=False,
    )
    amount = Column(Integer, nullable=False)
    kind = Column(Integer, nullable=False)
    entity_id = Column(Integer, ForeignKey("entities.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)

    entity = relationship("Entity", back_populates="investors")
    project = relationship("Project", back_populates="investors")
