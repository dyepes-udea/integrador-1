from sqlalchemy import Column, Enum, ForeignKey, Integer, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from app.repositories.postgresql.database import postgresql


class ProfessorProject(postgresql.base()):
    __tablename__ = "professors_projects"
    __table_args__ = (PrimaryKeyConstraint("professor_id", "project_id"),)

    professor_id = Column(Integer, ForeignKey("professors.id"), nullable=False)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    role = Column(
        Enum(
            "Asesor",
            "Auxiliar de investigación",
            "Coinvestigador",
            "Coordinador del proyecto",
            "Egresado",
            "Estudiante de pregrado",
            "Estudiante en formación (Doctorado)",
            "Estudiante en formación (Maestría)",
            "Investigador principal",
            "Jóven investigador",
            "Otros roles",
            name="project_role",
        ),
        nullable=False,
    )

    professor = relationship("Professor", back_populates="professors_projects")
    project = relationship("Project", back_populates="professors_projects")
