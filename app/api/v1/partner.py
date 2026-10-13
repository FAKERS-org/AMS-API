from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.permissions import Role, require_roles
from app.models.user import User
from app.repositories.partner import PartnerRepository
from app.schemas.partner import PartnerCreate, PartnerPagination, PartnerRead, PartnerUpdate
from app.services.partner_service import PartnerService

router = APIRouter()


def _service(db: AsyncSession = Depends(get_db)) -> PartnerService:
    return PartnerService(PartnerRepository(db))


def _require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    return require_roles(Role.ADMIN, Role.SUPER_ADMIN, Role.STAFF)(current_user)


@router.get("/setup-table")
async def setup_table(
    service: PartnerService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.setup_table()


@router.get("/setup")
async def setup(
    service: PartnerService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.setup()


@router.get("", response_model=PartnerPagination)
async def list_partners(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    limit: int | None = Query(None, ge=1, le=100),
    search: str | None = Query(None),
    partner_type: str | None = Query(None),
    is_active: bool | None = Query(None),
    service: PartnerService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    effective_limit = limit if limit is not None else page_size
    return await service.list_all(
        page=page,
        page_size=effective_limit,
        search=search,
        partner_type=partner_type,
        is_active=is_active,
    )


@router.get("/{partner_id}/view", response_model=PartnerRead)
async def view_partner(
    partner_id: int,
    service: PartnerService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.view(partner_id)


@router.get("/{partner_id}", response_model=PartnerRead)
async def get_partner(
    partner_id: int,
    service: PartnerService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.get_by_id(partner_id)


@router.post("", response_model=PartnerRead, status_code=status.HTTP_201_CREATED)
async def create_partner(
    data: PartnerCreate,
    service: PartnerService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.create(data)


@router.put("/{partner_id}", response_model=PartnerRead)
async def replace_partner(
    partner_id: int,
    data: PartnerUpdate,
    service: PartnerService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.update(partner_id, data)


@router.patch("/{partner_id}", response_model=PartnerRead)
async def update_partner(
    partner_id: int,
    data: PartnerUpdate,
    service: PartnerService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.update(partner_id, data)


@router.delete("/{partner_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_partner(
    partner_id: int,
    service: PartnerService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    await service.delete(partner_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
