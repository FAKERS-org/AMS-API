from datetime import datetime
from pydantic import BaseModel

from app.schemas.common import PaginationMeta


class PartnerRead(BaseModel):
    id: int
    name: str
    description: str | None = None
    photo: str | None = None
    website_url: str | None = None
    partner_type: str | None = None
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class PartnerCreate(BaseModel):
    name: str
    description: str | None = None
    photo: str | None = None
    website_url: str | None = None
    partner_type: str | None = None
    is_active: bool = True


class PartnerUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    photo: str | None = None
    website_url: str | None = None
    partner_type: str | None = None
    is_active: bool | None = None


class PartnerPagination(BaseModel):
    data: list[PartnerRead]
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
