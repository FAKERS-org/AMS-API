from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.permissions import Role, require_roles
from app.models.user import User
from app.repositories.course import CourseRepository
from app.schemas.course import CourseCreate, CoursePagination, CourseRead, CourseUpdate
from app.services.course_service import CourseService

router = APIRouter()


def _service(db: AsyncSession = Depends(get_db)) -> CourseService:
    return CourseService(CourseRepository(db))


def _require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    return require_roles(Role.ADMIN, Role.SUPER_ADMIN, Role.STAFF)(current_user)


@router.get("/setup-table")
async def setup_table(
    service: CourseService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.setup_table()


@router.get("/setup")
async def setup(
    service: CourseService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.setup()


@router.get("", response_model=CoursePagination)
async def list_courses(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    limit: int | None = Query(None, ge=1, le=100),
    search: str | None = Query(None),
    department_id: int | None = Query(None),
    is_published: bool | None = Query(None),
    service: CourseService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    effective_limit = limit if limit is not None else page_size
    return await service.list_all(
        page=page,
        page_size=effective_limit,
        search=search,
        department_id=department_id,
        is_published=is_published,
    )


@router.get("/{course_id}/view", response_model=CourseRead)
async def view_course(
    course_id: int,
    service: CourseService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.view(course_id)


@router.get("/{course_id}", response_model=CourseRead)
async def get_course(
    course_id: int,
    service: CourseService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.get_by_id(course_id)


@router.post("", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
async def create_course(
    data: CourseCreate,
    service: CourseService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.create(data)


@router.put("/{course_id}", response_model=CourseRead)
async def replace_course(
    course_id: int,
    data: CourseUpdate,
    service: CourseService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.update(course_id, data)


@router.patch("/{course_id}", response_model=CourseRead)
async def update_course(
    course_id: int,
    data: CourseUpdate,
    service: CourseService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.update(course_id, data)


@router.delete("/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(
    course_id: int,
    service: CourseService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    await service.delete(course_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
