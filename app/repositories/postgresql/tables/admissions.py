from sqlalchemy import Column, ForeignKey, Integer, SmallInteger
from sqlalchemy.orm import relationship

from app.repositories.postgresql.database import postgresql


class Admission(postgresql.base()):
    __tablename__ = "admissions"

    id = Column(Integer, primary_key=True)
    semester = Column(SmallInteger, nullable=False)
    year = Column(Integer, nullable=False)
    admitted_students = Column(Integer, nullable=False)
    transfer_admitted_students = Column(Integer, nullable=False)
    reentry_admitted_students = Column(Integer, nullable=False)
    enrolled_students = Column(Integer, nullable=False)
    program_id = Column(Integer, ForeignKey("programs.id"), nullable=False)

    program = relationship("Program", back_populates="admissions")
