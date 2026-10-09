from datetime import datetime
from pydantic import BaseModel


class CollaborationRead(BaseModel):
    id: int
    title: str
    description: str | None
    duration: str | None
    funding: str | None
    objective: str | None
    tag: str | None
    image: str | None
    url: str | None
    is_published: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class CollaborationCreate(BaseModel):
    title: str
    description: str | None = None
    duration: str | None = None
    funding: str | None = None
    objective: str | None = None
    tag: str | None = None
    image: str | None = None
    url: str | None = None
    is_published: bool = True


class CollaborationUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    duration: str | None = None
    funding: str | None = None
    objective: str | None = None
    tag: str | None = None
    image: str | None = None
    url: str | None = None
    is_published: bool | None = None


class CollaborationPagination(BaseModel):
    data: list[CollaborationRead]
    total: int
    page: int
    page_size: int
    total_pages: int

