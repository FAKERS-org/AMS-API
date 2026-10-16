from datetime import datetime
from pydantic import BaseModel

from app.schemas.common import PaginationMeta


class CollaborationRead(BaseModel):
    id: int
    title: str
    description: str | None = None
    duration: str | None = None
    funding: str | None = None
    objective: str | None = None
    tag: str | None = None
    image: str | None = None
    url: str | None = None
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
    meta: PaginationMeta | None = None

    def model_post_init(self, __context):
        if not self.meta:
            self.meta = PaginationMeta(
                currentPage=self.page,
                perPage=self.page_size,
                totalPages=self.total_pages,
                totalItems=self.total,
            )
