from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.permissions import Role, require_roles
from app.models.event import EventCategory
from app.models.user import User
from app.repositories.event import EventRepository
from app.schemas.event import EventCreate, EventPagination, EventRead, EventUpdate
from app.services.event_service import EventService

router = APIRouter()


def _service(db: AsyncSession = Depends(get_db)) -> EventService:
    return EventService(EventRepository(db))


def _require_admin(
    current_user: User = Depends(get_current_user),
) -> User:
    return require_roles(Role.ADMIN, Role.SUPER_ADMIN, Role.STAFF)(current_user)


@router.get("/setup-table")
async def setup_table(
    service: EventService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.setup_table()


@router.get("/setup")
async def setup(
    service: EventService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.setup()


@router.get("", response_model=EventPagination)
async def list_events(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    limit: int | None = Query(None, ge=1, le=100),
    search: str | None = Query(None),
    category: EventCategory | None = Query(None),
    is_published: bool | None = Query(None),
    service: EventService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    effective_limit = limit if limit is not None else page_size
    return await service.list_all(
        page=page,
        page_size=effective_limit,
        search=search,
        category=category,
        is_published=is_published,
    )


@router.get("/{event_id}/view", response_model=EventRead)
async def view_event(
    event_id: int,
    service: EventService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.view(event_id)


@router.get("/{event_id}", response_model=EventRead)
async def get_event(
    event_id: int,
    service: EventService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.get_by_id(event_id)


@router.post("", response_model=EventRead, status_code=status.HTTP_201_CREATED)
async def create_event(
    data: EventCreate,
    service: EventService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.create(data)


@router.put("/{event_id}", response_model=EventRead)
async def replace_event(
    event_id: int,
    data: EventUpdate,
    service: EventService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.update(event_id, data)


@router.patch("/{event_id}", response_model=EventRead)
async def update_event(
    event_id: int,
    data: EventUpdate,
    service: EventService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    return await service.update(event_id, data)


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: int,
    service: EventService = Depends(_service),
    _actor: User = Depends(_require_admin),
):
    await service.delete(event_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
