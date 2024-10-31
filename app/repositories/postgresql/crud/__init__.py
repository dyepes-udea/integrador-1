from .admissions import AdmissionCRUD
from .entities import EntityCRUD
from .evaluations import EvaluationCRUD
from .investors import InvestorCRUD
from .professors import ProfessorCRUD
from .professors_programs import ProfessorProgramCRUD
from .professors_projects import ProfessorProjectCRUD
from .professors_subjects import ProfessorSubjectCRUD
from .programs import ProgramCRUD
from .programs_subjects import ProgramSubjectCRUD
from .projects import ProjectCRUD
from .subjects import SubjectCRUD


__ALL__ = [
    "AdmissionCRUD",
    "EntityCRUD",
    "EvaluationCRUD",
    "InvestorCRUD",
    "ProfessorCRUD",
    "ProfessorProgramCRUD",
    "ProfessorProjectCRUD",
    "ProfessorSubjectCRUD",
    "ProgramCRUD",
    "ProgramSubjectCRUD",
    "ProjectCRUD",
    "SubjectCRUD",
]
