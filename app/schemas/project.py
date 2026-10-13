from datetime import datetime
from pydantic import BaseModel

from app.schemas.common import PaginationMeta


class ProjectRead(BaseModel):
    id: int
    title: str
    description: str | None = None
    partner: str | None = None
    duration: str | None = None
    funding: str | None = None
    investigators: str | None = None
    faculties: str | None = None
    students: str | None = None
    status: str
    is_published: bool
    created_at: datetime

    model_config = {"from_attributes": True}

    def model_post_init(self, __context):
        if not self.faculties and self.investigators:
            self.faculties = self.investigators
        if not self.investigators and self.faculties:
            self.investigators = self.faculties


class ProjectCreate(BaseModel):
    title: str
    description: str | None = None
    partner: str | None = None
    duration: str | None = None
    funding: str | None = None
    investigators: str | None = None
    faculties: str | None = None
    students: str | None = None
    status: str = "ongoing"
    is_published: bool = True

    def model_post_init(self, __context):
        if not self.investigators and self.faculties:
            self.investigators = self.faculties


class ProjectUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    partner: str | None = None
    duration: str | None = None
    funding: str | None = None
    investigators: str | None = None
    faculties: str | None = None
    students: str | None = None
    status: str | None = None
    is_published: bool | None = None

    def model_post_init(self, __context):
        if not self.investigators and self.faculties:
            self.investigators = self.faculties


class ProjectPagination(BaseModel):
    data: list[ProjectRead]
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
