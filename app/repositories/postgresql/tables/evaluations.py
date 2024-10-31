from sqlalchemy import JSON, Column, Enum, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.repositories.postgresql.database import postgresql


class Evaluation(postgresql.base()):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True)
    code = Column(Enum(name="evaluation_code"), nullable=False)
    evaluations = Column(JSON, nullable=False, default=dict())
    professor_subject_id = Column(Integer, ForeignKey("professors_subjects.id"), nullable=False)

    professor_subject = relationship("ProfessorSubject", back_populates="evaluation")
