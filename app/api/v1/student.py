from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.permissions import Role, require_roles
from app.models.user import User
from app.repositories.student import StudentRepository
from app.schemas.student import StudentCreate, StudentPagination, StudentRead, StudentUpdate
from app.services.student_service import StudentService

router = APIRouter()


def _service(db: AsyncSession = Depends(get_db)) -> StudentService:
    return StudentService(StudentRepository(db))


def _require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    return require_roles(Role.ADMIN, Role.SUPER_ADMIN, Role.STAFF)(current_user)


@router.get("/setup-table")
async def setup_table(
    service: StudentService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.setup_table()


@router.get("/setup")
async def setup(
    service: StudentService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.setup()


@router.get("", response_model=StudentPagination)
async def list_students(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    limit: int | None = Query(None, ge=1, le=100),
    search: str | None = Query(None),
    department_id: int | None = Query(None),
    year_level: int | None = Query(None),
    service: StudentService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    effective_limit = limit if limit is not None else page_size
    return await service.list_all(
        page=page,
        page_size=effective_limit,
        search=search,
        department_id=department_id,
        year_level=year_level,
    )


@router.get("/{student_id}/view", response_model=StudentRead)
async def view_student(
    student_id: int,
    service: StudentService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.view(student_id)


@router.get("/{student_id}", response_model=StudentRead)
async def get_student(
    student_id: int,
    service: StudentService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.get_by_id(student_id)


@router.post("", response_model=StudentRead, status_code=status.HTTP_201_CREATED)
async def create_student(
    data: StudentCreate,
    service: StudentService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.create(data)


@router.put("/{student_id}", response_model=StudentRead)
async def replace_student(
    student_id: int,
    data: StudentUpdate,
    service: StudentService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.update(student_id, data)


@router.patch("/{student_id}", response_model=StudentRead)
async def update_student(
    student_id: int,
    data: StudentUpdate,
    service: StudentService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.update(student_id, data)


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    student_id: int,
    service: StudentService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    await service.delete(student_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


