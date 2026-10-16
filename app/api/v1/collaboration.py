from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.permissions import Role, require_roles
from app.models.user import User
from app.repositories.collaboration import CollaborationRepository
from app.schemas.collaboration import (
    CollaborationCreate,
    CollaborationPagination,
    CollaborationRead,
    CollaborationUpdate,
)
from app.services.collaboration_service import CollaborationService

router = APIRouter()


def _service(db: AsyncSession = Depends(get_db)) -> CollaborationService:
    return CollaborationService(CollaborationRepository(db))


def _require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    return require_roles(Role.ADMIN, Role.SUPER_ADMIN, Role.STAFF)(current_user)


@router.get("/setup-table")
async def setup_table(
    service: CollaborationService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.setup_table()


@router.get("/setup")
async def setup(
    service: CollaborationService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.setup()


@router.get("", response_model=CollaborationPagination)
async def list_collaborations(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    limit: int | None = Query(None, ge=1, le=100),
    search: str | None = Query(None),
    is_published: bool | None = Query(None),
    service: CollaborationService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    effective_limit = limit if limit is not None else page_size
    return await service.list_all(
        page=page,
        page_size=effective_limit,
        search=search,
        is_published=is_published,
    )


@router.get("/{collaboration_id}/view", response_model=CollaborationRead)
async def view_collaboration(
    collaboration_id: int,
    service: CollaborationService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.view(collaboration_id)


@router.get("/{collaboration_id}", response_model=CollaborationRead)
async def get_collaboration(
    collaboration_id: int,
    service: CollaborationService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.get_by_id(collaboration_id)


@router.post("", response_model=CollaborationRead, status_code=status.HTTP_201_CREATED)
async def create_collaboration(
    data: CollaborationCreate,
    service: CollaborationService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.create(data)


@router.put("/{collaboration_id}", response_model=CollaborationRead)
async def replace_collaboration(
    collaboration_id: int,
    data: CollaborationUpdate,
    service: CollaborationService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.update(collaboration_id, data)


@router.patch("/{collaboration_id}", response_model=CollaborationRead)
async def update_collaboration(
    collaboration_id: int,
    data: CollaborationUpdate,
    service: CollaborationService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.update(collaboration_id, data)


@router.delete("/{collaboration_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collaboration(
    collaboration_id: int,
    service: CollaborationService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    await service.delete(collaboration_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
