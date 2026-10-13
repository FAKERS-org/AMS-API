from fastapi import APIRouter

from app.api.public import (
    announcement,
    award,
    collaboration,
    course,
    department,
    event,
    faculty,
    partner,
    project,
    scholarship,
    student,
)

public_router = APIRouter()

# ── AMS Public Endpoints (Exact match for AMS/api ams-public routes) ──
public_router.include_router(event.router, prefix="/events", tags=["AMS Public – Events"])
public_router.include_router(faculty.router, prefix="/faculties", tags=["AMS Public – Faculties"])
public_router.include_router(student.router, prefix="/students", tags=["AMS Public – Students"])
public_router.include_router(partner.router, prefix="/partners", tags=["AMS Public – Partners"])
public_router.include_router(course.router, prefix="/courses", tags=["AMS Public – Courses"])
public_router.include_router(scholarship.router, prefix="/scholarships", tags=["AMS Public – Scholarships"])
public_router.include_router(project.router, prefix="/projects", tags=["AMS Public – Projects"])
public_router.include_router(award.router, prefix="/awards", tags=["AMS Public – Awards"])
public_router.include_router(collaboration.router, prefix="/collaborations", tags=["AMS Public – Collaborations"])
public_router.include_router(department.router, prefix="/departments", tags=["AMS Public – Departments"])
public_router.include_router(announcement.router, prefix="/announcements", tags=["AMS Public – Announcements"])