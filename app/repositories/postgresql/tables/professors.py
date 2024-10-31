from sqlalchemy import VARCHAR, Column, Enum, Integer, Text
from sqlalchemy.orm import relationship

from app.repositories.postgresql.database import postgresql


class Professor(postgresql.base()):
    __tablename__ = "professors"

    id = Column(Integer, primary_key=True)
    identification_number = Column(VARCHAR(20), nullable=False, unique=True)
    identification_type = Column(
        Enum(
            "Cédula de ciudadanía",
            "Cédula de extranjería",
            "Pasaporte",
            name="professor_identification_type",
        ),
        nullable=False,
    )
    full_name = Column(Text, nullable=False)
    gender = Column(Enum("", "Hombre", "Mujer", name="professor_gender"), nullable=False)
    contract_type = Column(
        Enum("Docente de catedra", "Docente", name="professor_contract_type"),
        nullable=False,
    )
    employment_class = Column(
        Enum(
            "Aspirante",
            "Ocasional",
            "Externo",
            "Regular",
            "Empleado no docente",
            name="professor_employment_class",
        ),
        nullable=False,
    )
    institutional_email = Column(Text, nullable=True)

    professors_programs = relationship("ProfessorProgram", back_populates="professor")
    professors_subjects = relationship("ProfessorSubject", back_populates="professor")
    professors_projects = relationship("ProfessorProject", back_populates="professor")
