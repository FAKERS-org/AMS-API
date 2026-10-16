from fastapi import APIRouter

from app.api.v1.announcement import router as announcement_router
from app.api.v1.auth import router as auth_router
from app.api.v1.award import router as award_router
from app.api.v1.collaboration import router as collaboration_router
from app.api.v1.course import router as course_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.department import router as department_router
from app.api.v1.enrollment import router as enrollment_router
from app.api.v1.event import router as event_router
from app.api.v1.faculty import router as faculty_router
from app.api.v1.language import router as language_router
from app.api.v1.partner import router as partner_router
from app.api.v1.permission import router as permission_router
from app.api.v1.project import router as project_router
from app.api.v1.research_interest import router as research_interest_router
from app.api.v1.role import router as role_router
from app.api.v1.scholarship import router as scholarship_router
from app.api.v1.student import router as student_router
from app.api.v1.users import router as users_router

v1_router = APIRouter()

# ── 1. Core Auth, Users & Administration (Matching AMS/api) ──
v1_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
v1_router.include_router(users_router, prefix="/users", tags=["Users"])
v1_router.include_router(role_router, prefix="/roles", tags=["Roles"])
v1_router.include_router(permission_router, prefix="/permissions", tags=["Permissions"])
v1_router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
v1_router.include_router(dashboard_router, prefix="/dashoard", tags=["Dashboard"], include_in_schema=False)

# ── 2. University Domain Routes (Matching AMS/api /university/*) ──
university_router = APIRouter()
university_router.include_router(course_router, prefix="/courses", tags=["University – Courses"])
university_router.include_router(student_router, prefix="/students", tags=["University – Students"])
university_router.include_router(faculty_router, prefix="/faculties", tags=["University – Faculties"])
university_router.include_router(department_router, prefix="/categories", tags=["University – Categories"])
university_router.include_router(department_router, prefix="/departments", tags=["University – Departments"], include_in_schema=False)
university_router.include_router(project_router, prefix="/projects", tags=["University – Projects"])
university_router.include_router(award_router, prefix="/awards", tags=["University – Awards"])
university_router.include_router(event_router, prefix="/events", tags=["University – Events"])
university_router.include_router(language_router, prefix="/languages", tags=["University – Languages"])
university_router.include_router(partner_router, prefix="/partners", tags=["University – Partners"])
university_router.include_router(collaboration_router, prefix="/collaborations", tags=["University – Collaborations"])
university_router.include_router(scholarship_router, prefix="/scholarships", tags=["University – Scholarships"])
university_router.include_router(research_interest_router, prefix="/research-interests", tags=["University – Research Interests"])
university_router.include_router(enrollment_router, prefix="/enrollments", tags=["University – Enrollments"])
university_router.include_router(announcement_router, prefix="/announcements", tags=["University – Announcements"])

v1_router.include_router(university_router, prefix="/university")

# ── Flat aliases for backwards compatibility (hidden from Swagger docs) ──
v1_router.include_router(course_router, prefix="/courses", include_in_schema=False)
v1_router.include_router(student_router, prefix="/students", include_in_schema=False)
v1_router.include_router(faculty_router, prefix="/faculties", include_in_schema=False)
v1_router.include_router(department_router, prefix="/departments", include_in_schema=False)
v1_router.include_router(project_router, prefix="/projects", include_in_schema=False)
v1_router.include_router(award_router, prefix="/awards", include_in_schema=False)
v1_router.include_router(event_router, prefix="/events", include_in_schema=False)
v1_router.include_router(language_router, prefix="/languages", include_in_schema=False)
v1_router.include_router(partner_router, prefix="/partners", include_in_schema=False)
v1_router.include_router(collaboration_router, prefix="/collaborations", include_in_schema=False)
v1_router.include_router(scholarship_router, prefix="/scholarships", include_in_schema=False)
v1_router.include_router(research_interest_router, prefix="/research-interests", include_in_schema=False)
v1_router.include_router(enrollment_router, prefix="/enrollments", include_in_schema=False)
v1_router.include_router(announcement_router, prefix="/announcements", include_in_schema=False)
