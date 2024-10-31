from fastapi import APIRouter

from app.api.endpoints import (
    admissions,
    health_check,
    investors,
    professors,
    programs,
    projects,
    subjects,
    professors_subjects,
)


router = APIRouter()

router.include_router(health_check.router, prefix="/health-check", tags=["Health Check"])
router.include_router(professors.router, prefix="/professors", tags=["Professors"])
router.include_router(programs.router, prefix="/programs", tags=["Programs"])
router.include_router(admissions.router, prefix="/admissions", tags=["Admissions"])
router.include_router(subjects.router, prefix="/subjects", tags=["Subjects"])
router.include_router(projects.router, prefix="/projects", tags=["Projects"])
router.include_router(investors.router, prefix="/investors", tags=["Investors"])
router.include_router(professors_subjects.router, prefix="/professors-subjects", tags=["Professors Subjects"])
