from sqlalchemy import Column, Double, Enum, ForeignKey, Integer, SmallInteger, UniqueConstraint
from sqlalchemy.orm import relationship

from app.repositories.postgresql.database import postgresql


class ProfessorSubject(postgresql.base()):
    __tablename__ = "professors_subjects"
    __table_args__ = (
        UniqueConstraint(
            "professor_id",
            "subject_id",
            "semester",
            "year",
            "group",
            name="uix_professor_subject_semester_year_group",
        ),
    )

    id = Column(Integer, primary_key=True)
    professor_id = Column(Integer, ForeignKey("professors.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    semester = Column(SmallInteger, nullable=False)
    year = Column(Integer, nullable=False)
    group = Column(SmallInteger, nullable=False)
    location = Column(
        Enum(
            "Salón",
            "Ude@",
            "Ingenia",
            "Ingenia y Salón",
            name="professor_subject_location"
        ),
        nullable=False,
    )
    available_spots = Column(SmallInteger, nullable=False)
    enrolled_students = Column(SmallInteger, nullable=False)
    cancelled_students = Column(SmallInteger, nullable=False)
    missed_students = Column(SmallInteger, nullable=False)
    avg_note = Column(Double, nullable=False)
    stddev_note = Column(Double, nullable=False)

    professor = relationship("Professor", back_populates="professors_subjects")
    subject = relationship("Subject", back_populates="professors_subjects")
    evaluation = relationship("Evaluation", back_populates="professor_subject")
