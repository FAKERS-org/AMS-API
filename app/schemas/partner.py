from datetime import datetime
from pydantic import BaseModel


class PartnerRead(BaseModel):
    id: int
    name: str
    description: str | None
    photo: str | None
    website_url: str | None
    partner_type: str | None
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

