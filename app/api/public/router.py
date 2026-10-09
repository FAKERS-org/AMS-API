from fastapi import APIRouter

from app.api.public import (
    announcement,
    award,
    collaboration,
    course,
    event,
    faculty,
    partner,
    project,
    scholarship,
    student,
)

public_router = APIRouter()

public_router.include_router(announcement.router, prefix="/announcements", tags=["Public – Announcements"])
public_router.include_router(course.router, prefix="/courses", tags=["Public – Courses"])
public_router.include_router(faculty.router, prefix="/faculties", tags=["Public – Faculty"])
public_router.include_router(event.router, prefix="/events", tags=["Public – Events"])
public_router.include_router(scholarship.router, prefix="/scholarships", tags=["Public – Scholarships"])
public_router.include_router(partner.router, prefix="/partners", tags=["Public – Partners"])
public_router.include_router(project.router, prefix="/projects", tags=["Public – Projects"])
public_router.include_router(award.router, prefix="/awards", tags=["Public – Awards"])
public_router.include_router(collaboration.router, prefix="/collaborations", tags=["Public – Collaborations"])
public_router.include_router(student.router, prefix="/students", tags=["Public – Students"])