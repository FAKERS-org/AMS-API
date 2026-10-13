from datetime import datetime
from pydantic import BaseModel

from app.schemas.common import PaginationMeta


class ScholarshipContact(BaseModel):
    office: str | None = None
    email: str | None = None
    phone: str | None = None


class ScholarshipRead(BaseModel):
    id: int
    title: str
    description: str | None = None
    amount: str | None = None
    duration: str | None = None
    eligibility: str | None = None
    application_process: str | None = None
    contact_office: str | None = None
    contact_email: str | None = None
    contact_phone: str | None = None
    deadline: datetime | None = None
    is_published: bool
    created_at: datetime
    name: str | None = None

    model_config = {"from_attributes": True}

    def model_post_init(self, __context):
        if not self.name:
            self.name = self.title


class ScholarshipCreate(BaseModel):
    title: str | None = None
    name: str | None = None
    description: str | None = None
    amount: str | None = None
    duration: str | None = None
    eligibility: str | None = None
    application_process: str | None = None
    contact_office: str | None = None
    contact_email: str | None = None
    contact_phone: str | None = None
    deadline: datetime | None = None
    is_published: bool = True

    def model_post_init(self, __context):
        if not self.title and self.name:
            self.title = self.name
        elif not self.title:
            self.title = "Scholarship"


class ScholarshipUpdate(BaseModel):
    title: str | None = None
    name: str | None = None
    description: str | None = None
    amount: str | None = None
    duration: str | None = None
    eligibility: str | None = None
    application_process: str | None = None
    contact_office: str | None = None
    contact_email: str | None = None
    contact_phone: str | None = None
    deadline: datetime | None = None
    is_published: bool | None = None

    def model_post_init(self, __context):
        if not self.title and self.name:
            self.title = self.name


class ScholarshipPagination(BaseModel):
    data: list[ScholarshipRead]
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
