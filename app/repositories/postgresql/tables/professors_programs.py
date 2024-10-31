from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from app.repositories.postgresql.database import postgresql


class ProfessorProgram(postgresql.base()):
    __tablename__ = "professors_programs"
    __table_args__ = (PrimaryKeyConstraint("professor_id", "program_id"),)

    professor_id = Column(Integer, ForeignKey("professors.id"), nullable=False)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=False)

    professor = relationship("Professor", back_populates="professors_programs")
    program = relationship("Program", back_populates="professors_programs")
