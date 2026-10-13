from datetime import datetime
from pydantic import BaseModel

from app.schemas.common import PaginationMeta


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


class AnnouncementPagination(BaseModel):
    data: list[AnnouncementRead]
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
