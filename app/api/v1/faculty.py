from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.permissions import Role, require_roles
from app.models.user import User
from app.repositories.faculty import FacultyRepository
from app.schemas.faculty import (
    CourseFacultyCreate,
    CourseFacultyRead,
    FacultyCreate,
    FacultyPagination,
    FacultyRead,
    FacultyUpdate,
)
from app.services.faculty_service import FacultyService

router = APIRouter()


def _service(db: AsyncSession = Depends(get_db)) -> FacultyService:
    return FacultyService(FacultyRepository(db))


def _require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    return require_roles(Role.ADMIN, Role.SUPER_ADMIN, Role.STAFF)(current_user)


@router.get("/setup-table")
async def setup_table(
    service: FacultyService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.setup_table()


@router.get("/setup")
async def setup(
    service: FacultyService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.setup()


@router.get("", response_model=FacultyPagination)
async def list_faculty(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    limit: int | None = Query(None, ge=1, le=100),
    search: str | None = Query(None),
    department_id: int | None = Query(None),
    is_active: bool | None = Query(None),
    service: FacultyService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    effective_limit = limit if limit is not None else page_size
    return await service.list_all(
        page=page,
        page_size=effective_limit,
        search=search,
        department_id=department_id,
        is_active=is_active,
    )


@router.get("/{faculty_id}/view", response_model=FacultyRead)
async def view_faculty(
    faculty_id: int,
    service: FacultyService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.view(faculty_id)


@router.get("/{faculty_id}", response_model=FacultyRead)
async def get_faculty(
    faculty_id: int,
    service: FacultyService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.get_by_id(faculty_id)


@router.post("", response_model=FacultyRead, status_code=status.HTTP_201_CREATED)
async def create_faculty(
    data: FacultyCreate,
    service: FacultyService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.create(data)


@router.put("/{faculty_id}", response_model=FacultyRead)
async def replace_faculty(
    faculty_id: int,
    data: FacultyUpdate,
    service: FacultyService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.update(faculty_id, data)


@router.patch("/{faculty_id}", response_model=FacultyRead)
async def update_faculty(
    faculty_id: int,
    data: FacultyUpdate,
    service: FacultyService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.update(faculty_id, data)


@router.delete("/{faculty_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_faculty(
    faculty_id: int,
    service: FacultyService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    await service.delete(faculty_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{faculty_id}/assignments",
    response_model=CourseFacultyRead,
    status_code=status.HTTP_201_CREATED,
)
async def assign_course(
    faculty_id: int,
    data: CourseFacultyCreate,
    service: FacultyService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.assign_course(faculty_id, data)


@router.delete(
    "/{faculty_id}/assignments/{assignment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_assignment(
    faculty_id: int,
    assignment_id: int,
    service: FacultyService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    await service.remove_assignment(faculty_id, assignment_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
