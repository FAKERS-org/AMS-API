from datetime import datetime
from pydantic import BaseModel


class ProjectRead(BaseModel):
    id: int
    title: str
    description: str | None
    partner: str | None
    duration: str | None
    funding: str | None
    investigators: str | None
    students: str | None
    status: str
    is_published: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class ProjectCreate(BaseModel):
    title: str
    description: str | None = None
    partner: str | None = None
    duration: str | None = None
    funding: str | None = None
    investigators: str | None = None
    students: str | None = None
    status: str = "ongoing"
    is_published: bool = True


class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    partner: str | None = None
    duration: str | None = None
    funding: str | None = None
    investigators: str | None = None
    students: str | None = None
    status: str | None = None
    is_published: bool | None = None


class ProjectPagination(BaseModel):
    data: list[ProjectRead]
    total: int
    page: int
    page_size: int
    total_pages: int

