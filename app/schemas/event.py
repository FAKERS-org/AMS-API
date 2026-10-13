from datetime import datetime
from pydantic import BaseModel

from app.models.event import EventCategory
from app.schemas.common import PaginationMeta


class EventRead(BaseModel):
    id: int
    title: str
    category: EventCategory
    description: str | None = None
    preview: str | None = None
    published_by: str | None = None
    location: str | None = None
    tag: str | None = None
    photo: str | None = None
    event_url: str | None = None
    published_date: datetime | None = None
    status: str
    is_published: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class EventCreate(BaseModel):
    title: str
    category: EventCategory = EventCategory.EVENTS
    description: str | None = None
    preview: str | None = None
    published_by: str | None = None
    location: str | None = None
    tag: str | None = None
    photo: str | None = None
    event_url: str | None = None
    published_date: datetime | None = None
    status: str = "active"
    is_published: bool = True


class EventUpdate(BaseModel):
    title: str | None = None
    category: EventCategory | None = None
    description: str | None = None
    preview: str | None = None
    published_by: str | None = None
    location: str | None = None
    tag: str | None = None
    photo: str | None = None
    event_url: str | None = None
    published_date: datetime | None = None
    status: str | None = None
    is_published: bool | None = None


class EventPagination(BaseModel):
    data: list[EventRead]
    total: int
    page: int
    page_size: int
    total_pages: int
    meta: PaginationMeta | None = None

    def model_post_init(self, __context):
        if not self.meta:
            self.meta = PaginationMeta(
                currentPage=self.page,
                perPage=self.page_size,
                totalPages=self.total_pages,
                totalItems=self.total,
            )
