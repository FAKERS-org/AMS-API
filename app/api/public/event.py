from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.event import EventCategory
from app.repositories.event import EventRepository
from app.schemas.event import EventPagination, EventRead
from app.services.event_service import EventService

router = APIRouter()


def _service(db: AsyncSession = Depends(get_db)) -> EventService:
    return EventService(EventRepository(db))


@router.get("", response_model=EventPagination)
async def list_public_events(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    category: EventCategory | None = Query(None),
    service: EventService = Depends(_service),
):
    return await service.list_published(
        page=page,
        page_size=page_size,
        search=search,
        category=category,
    )


@router.get("/news", response_model=EventPagination)
async def list_public_news(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    service: EventService = Depends(_service),
):
    return await service.list_published(
        page=page,
        page_size=page_size,
        search=search,
        category=EventCategory.NEWS,
    )


@router.get("/events", response_model=EventPagination)
async def list_public_event_category(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str | None = Query(None),
    service: EventService = Depends(_service),
):
    return await service.list_published(
        page=page,
        page_size=page_size,
        search=search,
        category=EventCategory.EVENTS,
    )


@router.get("/{event_id}", response_model=EventRead)
async def get_public_event(
    event_id: int,
    service: EventService = Depends(_service),
):
    return await service.get_published_by_id(event_id)

