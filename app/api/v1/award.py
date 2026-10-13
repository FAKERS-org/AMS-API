from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.permissions import Role, require_roles
from app.models.user import User
from app.repositories.award import AwardRepository
from app.schemas.award import AwardCreate, AwardPagination, AwardRead, AwardUpdate
from app.services.award_service import AwardService

router = APIRouter()


def _service(db: AsyncSession = Depends(get_db)) -> AwardService:
    return AwardService(AwardRepository(db))


def _require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    return require_roles(Role.ADMIN, Role.SUPER_ADMIN, Role.STAFF)(current_user)


@router.get("/setup-table")
async def setup_table(
    service: AwardService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.setup_table()


@router.get("/setup")
async def setup(
    service: AwardService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.setup()


@router.get("", response_model=AwardPagination)
async def list_awards(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    limit: int | None = Query(None, ge=1, le=100),
    search: str | None = Query(None),
    is_published: bool | None = Query(None),
    service: AwardService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    effective_limit = limit if limit is not None else page_size
    return await service.list_all(
        page=page,
        page_size=effective_limit,
        search=search,
        is_published=is_published,
    )


@router.get("/{award_id}/view", response_model=AwardRead)
async def view_award(
    award_id: int,
    service: AwardService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.view(award_id)


@router.get("/{award_id}", response_model=AwardRead)
async def get_award(
    award_id: int,
    service: AwardService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.get_by_id(award_id)


@router.post("", response_model=AwardRead, status_code=status.HTTP_201_CREATED)
async def create_award(
    data: AwardCreate,
    service: AwardService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.create(data)


@router.put("/{award_id}", response_model=AwardRead)
async def replace_award(
    award_id: int,
    data: AwardUpdate,
    service: AwardService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.update(award_id, data)


@router.patch("/{award_id}", response_model=AwardRead)
async def update_award(
    award_id: int,
    data: AwardUpdate,
    service: AwardService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.update(award_id, data)


@router.delete("/{award_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_award(
    award_id: int,
    service: AwardService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    await service.delete(award_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
