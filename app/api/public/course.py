from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.repositories.course import CourseRepository
from app.schemas.course import CoursePagination, CourseRead
from app.services.course_service import CourseService

router = APIRouter()


def _service(db: AsyncSession = Depends(get_db)) -> CourseService:
    return CourseService(CourseRepository(db))


@router.get("", response_model=CoursePagination)
async def list_public_courses(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    department_id: int | None = Query(None),
    service: CourseService = Depends(_service),
):
    return await service.list_published(
        page=page,
        page_size=page_size,
        search=search,
        department_id=department_id,
    )


@router.get("/{course_id}", response_model=CourseRead)
async def get_public_course(
    course_id: int,
    service: CourseService = Depends(_service),
):
    return await service.get_published_by_id(course_id)

