from app.core.exceptions import AppException
from app.models.event import EventCategory
from app.repositories.event import EventRepository
from app.schemas.event import EventCreate, EventUpdate


class EventService:
    def __init__(self, repo: EventRepository):
        self.repo = repo

    async def setup_table(self):
        return [
            {"value": "title", "label": "Title", "type": "text"},
            {"value": "category", "label": "Category", "type": "text"},
            {"value": "description", "label": "Description", "type": "text"},
            {"value": "preview", "label": "Preview", "type": "text"},
            {"value": "published_by", "label": "Published By", "type": "text"},
            {"value": "location", "label": "Location", "type": "text"},
            {"value": "tag", "label": "Tag", "type": "text"},
            {"value": "status", "label": "Status", "type": "text"},
            {"value": "photo", "label": "Photo", "type": "image"},
            {"value": "actions", "label": "Actions", "type": "actions"},
        ]

    async def setup(self):
        return {
            "name": "Event",
            "fields": [
                {"name": "title", "value": "title", "type": "text", "label": "Title", "is_required": True},
                {
                    "name": "category",
                    "value": "category",
                    "type": "select",
                    "label": "Category",
                    "options": [
                        {"value": "news", "label": "News"},
                        {"value": "events", "label": "Events"},
                        {"value": "announcements", "label": "Announcements"},
                    ],
                },
                {"name": "location", "value": "location", "type": "text", "label": "Location"},
                {"name": "published_by", "value": "published_by", "type": "text", "label": "Published By"},
                {"name": "tag", "value": "tag", "type": "text", "label": "Tag"},
                {"name": "photo", "value": "photo", "label": "Photo", "type": "image"},
                {"name": "event_url", "value": "event_url", "type": "text", "label": "Event URL"},
                {"name": "preview", "value": "preview", "type": "textarea", "label": "Preview"},
                {"name": "description", "value": "description", "type": "textarea", "label": "Description"},
            ],
        }

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

    async def list_all(
        self,
        page: int = 1,
        page_size: int = 20,
        search: str | None = None,
        category: EventCategory | None = None,
        is_published: bool | None = None,
    ):
        return await self.repo.list_all(
            page=page,
            page_size=page_size,
            search=search,
            category=category,
            is_published=is_published,
        )

    async def get_published_by_id(self, event_id: int):
        event = await self.repo.get_published_by_id(event_id)
        if not event:
            raise AppException(404, "Event not found")
        return event

    async def get_by_id(self, event_id: int):
        event = await self.repo.get_by_id(event_id)
        if not event:
            raise AppException(404, "Event not found")
        return event

    async def view(self, event_id: int):
        return await self.get_by_id(event_id)

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
