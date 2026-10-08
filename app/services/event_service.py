from app.core.exceptions import AppException
from app.models.event import EventCategory
from app.repositories.event import EventRepository
from app.schemas.event import EventCreate, EventUpdate


class EventService:
    def __init__(self, repo: EventRepository):
        self.repo = repo

    async def list_published(
        self,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        category: EventCategory | None = None,
    ):
        return await self.repo.get_published(
            page=page,
            page_size=page_size,
            search=search,
            category=category,
        )

    async def get_published_by_id(self, event_id: int):
        event = await self.repo.get_published_by_id(event_id)
        if not event:
            raise AppException(404, "Event not found")
        return event

    async def create(self, data: EventCreate):
        return await self.repo.create(data.model_dump())

    async def update(self, event_id: int, data: EventUpdate):
        event = await self.repo.get_by_id(event_id)
        if not event:
            raise AppException(404, "Event not found")
        return await self.repo.update(event, data.model_dump(exclude_unset=True))

    async def delete(self, event_id: int):
        event = await self.repo.get_by_id(event_id)
        if not event:
            raise AppException(404, "Event not found")
        await self.repo.delete(event)

