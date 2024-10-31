from sqlalchemy import Column, Enum, Integer, Text
from sqlalchemy.orm import relationship

from app.repositories.postgresql.database import postgresql


class Program(postgresql.base()):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True)
    code = Column(Integer, nullable=False, unique=True)
    name = Column(Text, nullable=False)
    type = Column(
        Enum(
            "Pregrado",
            "Especialización",
            "Maestria",
            "Doctorado",
            name="program_type",
        ),
        nullable=False,
    )
    modality = Column(
        Enum("Presencial", "Virtual", name="program_modality"), nullable=False,
    )

    professors_programs = relationship("ProfessorProgram", back_populates="program")
    programs_subjects = relationship("ProgramSubject", back_populates="program")
    admissions = relationship("Admission", back_populates="program")
