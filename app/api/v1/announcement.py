from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.permissions import Role, require_roles
from app.models.user import User
from app.repositories.announcement import AnnouncementRepository
from app.schemas.announcement import (
    AnnouncementCreate,
    AnnouncementPagination,
    AnnouncementRead,
    AnnouncementUpdate,
)
from app.services.announcement_service import AnnouncementService

router = APIRouter()


def _service(db: AsyncSession = Depends(get_db)) -> AnnouncementService:
    return AnnouncementService(AnnouncementRepository(db))


def _require_staff_or_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    return require_roles(Role.ADMIN, Role.SUPER_ADMIN, Role.STAFF, Role.FACULTY)(current_user)


@router.get("", response_model=AnnouncementPagination)
async def list_announcements(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    is_published: bool | None = Query(None),
    service: AnnouncementService = Depends(_service),
    _actor: User = Depends(_require_staff_or_admin),
):
    return await service.list_all(
        page=page,
        page_size=page_size,
        search=search,
        is_published=is_published,
    )


@router.get("/{announcement_id}", response_model=AnnouncementRead)
async def get_announcement(
    announcement_id: int,
    service: AnnouncementService = Depends(_service),
    _actor: User = Depends(_require_staff_or_admin),
):
    return await service.get_by_id(announcement_id)


@router.post("", response_model=AnnouncementRead, status_code=status.HTTP_201_CREATED)
async def create_announcement(
    data: AnnouncementCreate,
    service: AnnouncementService = Depends(_service),
    actor: User = Depends(_require_staff_or_admin),
):
    return await service.create(data, author_id=actor.id)


@router.patch("/{announcement_id}", response_model=AnnouncementRead)
async def update_announcement(
    announcement_id: int,
    data: AnnouncementUpdate,
    service: AnnouncementService = Depends(_service),
    _actor: User = Depends(_require_staff_or_admin),
):
    return await service.update(announcement_id, data)


@router.delete("/{announcement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_announcement(
    announcement_id: int,
    service: AnnouncementService = Depends(_service),
    _actor: User = Depends(_require_staff_or_admin),
):
    await service.delete(announcement_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

