from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.permissions import Role, require_roles
from app.models.user import User
from app.repositories.scholarship import ScholarshipRepository
from app.schemas.scholarship import (
    ScholarshipCreate,
    ScholarshipPagination,
    ScholarshipRead,
    ScholarshipUpdate,
)
from app.services.scholarship_service import ScholarshipService

router = APIRouter()


def _service(db: AsyncSession = Depends(get_db)) -> ScholarshipService:
    return ScholarshipService(ScholarshipRepository(db))


def _require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    return require_roles(Role.ADMIN, Role.SUPER_ADMIN, Role.STAFF)(current_user)


@router.get("/setup-table")
async def setup_table(
    service: ScholarshipService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.setup_table()


@router.get("/setup")
async def setup(
    service: ScholarshipService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.setup()


@router.get("", response_model=ScholarshipPagination)
async def list_scholarships(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    limit: int | None = Query(None, ge=1, le=100),
    search: str | None = Query(None),
    is_published: bool | None = Query(None),
    service: ScholarshipService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    effective_limit = limit if limit is not None else page_size
    return await service.list_all(
        page=page,
        page_size=effective_limit,
        search=search,
        is_published=is_published,
    )


@router.get("/{scholarship_id}/view", response_model=ScholarshipRead)
async def view_scholarship(
    scholarship_id: int,
    service: ScholarshipService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.view(scholarship_id)


@router.get("/{scholarship_id}", response_model=ScholarshipRead)
async def get_scholarship(
    scholarship_id: int,
    service: ScholarshipService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.get_by_id(scholarship_id)


@router.post("", response_model=ScholarshipRead, status_code=status.HTTP_201_CREATED)
async def create_scholarship(
    data: ScholarshipCreate,
    service: ScholarshipService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.create(data)


@router.put("/{scholarship_id}", response_model=ScholarshipRead)
async def replace_scholarship(
    scholarship_id: int,
    data: ScholarshipUpdate,
    service: ScholarshipService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.update(scholarship_id, data)


@router.patch("/{scholarship_id}", response_model=ScholarshipRead)
async def update_scholarship(
    scholarship_id: int,
    data: ScholarshipUpdate,
    service: ScholarshipService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.update(scholarship_id, data)


@router.delete("/{scholarship_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_scholarship(
    scholarship_id: int,
    service: ScholarshipService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    await service.delete(scholarship_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
