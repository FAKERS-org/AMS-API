from datetime import datetime
from pydantic import BaseModel


class AnnouncementRead(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    is_published: bool
    is_pinned: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class AnnouncementCreate(BaseModel):
    title: str
    content: str
    is_pinned: bool = False


class AnnouncementUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    is_published: bool | None = None
    is_pinned: bool | None = None
