from sqlalchemy import Column, ForeignKey, Integer, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from app.repositories.postgresql.database import postgresql


class ProgramSubject(postgresql.base()):
    __tablename__ = "programs_subjects"
    __table_args__ = (PrimaryKeyConstraint("subject_id", "program_id"),)

    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=False)

    subject = relationship("Subject", back_populates="programs_subjects")
    program = relationship("Program", back_populates="programs_subjects")
