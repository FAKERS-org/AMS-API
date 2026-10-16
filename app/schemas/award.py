from datetime import datetime
from pydantic import BaseModel

from app.schemas.common import PaginationMeta


class AwardRead(BaseModel):
    id: int
    title: str
    description: str | None = None
    achievement: str | None = None
    imagepath: str | None = None
    recipient_name: str | None = None
    student_id: int | None = None
    award_date: datetime | None = None
    is_published: bool
    created_at: datetime
    student: str | None = None
    image: str | None = None

    model_config = {"from_attributes": True}

    def model_post_init(self, __context):
        if not self.student and self.recipient_name:
            self.student = self.recipient_name
        if not self.image and self.imagepath:
            self.image = self.imagepath


class AwardCreate(BaseModel):
    title: str
    description: str | None = None
    achievement: str | None = None
    imagepath: str | None = None
    image: str | None = None
    recipient_name: str | None = None
    student: str | None = None
    student_id: int | None = None
    award_date: datetime | None = None
    is_published: bool = True

    def model_post_init(self, __context):
        if not self.imagepath and self.image:
            self.imagepath = self.image
        if not self.recipient_name and self.student:
            self.recipient_name = self.student


class AwardUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    achievement: str | None = None
    imagepath: str | None = None
    image: str | None = None
    recipient_name: str | None = None
    student: str | None = None
    student_id: int | None = None
    award_date: datetime | None = None
    is_published: bool | None = None

    def model_post_init(self, __context):
        if not self.imagepath and self.image:
            self.imagepath = self.image
        if not self.recipient_name and self.student:
            self.recipient_name = self.student


class AwardPagination(BaseModel):
    data: list[AwardRead]
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
