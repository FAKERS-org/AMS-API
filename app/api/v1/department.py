from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.permissions import Role, require_roles
from app.models.user import User
from app.repositories.department import DepartmentRepository
from app.schemas.department import (
    DepartmentCreate,
    DepartmentDetailRead,
    DepartmentPagination,
    DepartmentRead,
    DepartmentUpdate,
)
from app.services.department_service import DepartmentService

router = APIRouter()


def _service(db: AsyncSession = Depends(get_db)) -> DepartmentService:
    return DepartmentService(DepartmentRepository(db))


def _require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    return require_roles(Role.ADMIN, Role.SUPER_ADMIN, Role.STAFF)(current_user)


@router.get("/setup-table")
async def setup_table(
    service: DepartmentService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.setup_table()


@router.get("/setup")
async def setup(
    service: DepartmentService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.setup()


@router.get("", response_model=DepartmentPagination)
async def list_departments(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    limit: int | None = Query(None, ge=1, le=100),
    search: str | None = Query(None),
    service: DepartmentService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    effective_limit = limit if limit is not None else page_size
    return await service.list(
        page=page,
        page_size=effective_limit,
        search=search,
    )


@router.get("/{department_id}/view", response_model=DepartmentDetailRead)
async def view_department(
    department_id: int,
    service: DepartmentService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.view(department_id)


@router.get("/{department_id}", response_model=DepartmentDetailRead)
async def get_department(
    department_id: int,
    service: DepartmentService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.get_detail(department_id)


@router.post("", response_model=DepartmentRead, status_code=status.HTTP_201_CREATED)
async def create_department(
    data: DepartmentCreate,
    service: DepartmentService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.create(data)


@router.put("/{department_id}", response_model=DepartmentRead)
async def replace_department(
    department_id: int,
    data: DepartmentUpdate,
    service: DepartmentService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.update(department_id, data)


@router.patch("/{department_id}", response_model=DepartmentRead)
async def update_department(
    department_id: int,
    data: DepartmentUpdate,
    service: DepartmentService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.update(department_id, data)


@router.delete("/{department_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_department(
    department_id: int,
    service: DepartmentService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    await service.delete(department_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
