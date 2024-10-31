from sqlalchemy import ARRAY, Boolean, Column, Integer, SmallInteger, Text
from sqlalchemy.orm import relationship

from app.repositories.postgresql.database import postgresql


class Subject(postgresql.base()):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    code = Column(Integer, nullable=False, unique=True)
    name = Column(Text, nullable=False)
    credits = Column(SmallInteger, nullable=False)
    is_enabled = Column(Boolean, nullable=False)
    study_plan_version = Column(ARRAY(SmallInteger), nullable=False, default=list())
    description = Column(Text, nullable=True)

    programs_subjects = relationship("ProgramSubject", back_populates="subject")
    professors_subjects = relationship("ProfessorSubject", back_populates="subject")
