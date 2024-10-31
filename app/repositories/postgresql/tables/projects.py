from sqlalchemy import ARRAY, JSON, Column, Date, Enum, Integer, Text
from sqlalchemy.orm import relationship

from app.repositories.postgresql.database import postgresql


class Project(postgresql.base()):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    code = Column(Integer, nullable=False, unique=True)
    name = Column(Text, nullable=False)
    status = Column(
        Enum(
            "Aprobado",
            "En Ejecución",
            "Finalizado",
            "Liquidado",
            "Pendiente de Programación",
            name="project_status",
        ),
        nullable=False,
    )
    call = Column(Text, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    members = Column(ARRAY(JSON), nullable=False, default=list())

    investors = relationship("Investor", back_populates="project")
    professors_projects = relationship("ProfessorProject", back_populates="project")
