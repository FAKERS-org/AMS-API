from datetime import datetime
from pydantic import BaseModel

from app.models.event import EventCategory


class EventRead(BaseModel):
    id: int
    title: str
    category: EventCategory
    description: str | None
    preview: str | None
    published_by: str | None
    location: str | None
    tag: str | None
    photo: str | None
    event_url: str | None
    published_date: datetime | None
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

